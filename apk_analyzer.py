import datetime
import glob
import itertools
import logging
import os
import subprocess

import numpy as np
import string_classifier
from classifier_singleton import classifier
from elftools.common.exceptions import ELFError
from flufl.lock import Lock, AlreadyLockedError, TimeOutError
from strings_filter_singleton import s_filter

from config import conf
from my_model.lib_string import LibString
from my_model.resource_string import ResourceString
from my_tools.apktool_yml_parser import ApktoolYmlParser
from my_tools.manifest_parser import AndroidManifestXmlParser
from my_tools.smali_parser import SmaliParser
from my_tools.strings_tool import strings
from my_tools.strings_xml_parser import AndroidStringsXmlParser

LOCK_PREFIX = ".lock"
logging.getLogger("flufl.lock").setLevel(logging.CRITICAL)  # disable logging for lock module

lib_blacklist = None
if conf.lib_blacklists:
    lib_blacklist = set()
    for txt in conf.lib_blacklists:
        for line in open(txt, "r"):
            lib_blacklist.add(line.replace('\n', '').replace('\r', ''))


class ApkAnalysisError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_next_apk(apks_dir):
    """
    Gets the first available (not-locked) apk files and locks it

    :param apks_dir: directory to scan
    :return: a tuple containing the apk's path and the locked lock
    :rtype: (str, lockfile.LockFile)
    """
    try:
        files = os.listdir(apks_dir)
    except FileNotFoundError:
        # folder doesn't exist
        return None, None
    for f in files:
        if not f.endswith(".apk"):
            continue
        f = os.path.join(apks_dir, f)
        try:
            # lock file should not exist
            filename = f + LOCK_PREFIX

            lock = Lock(filename, lifetime=datetime.timedelta(seconds=6000))  # expires in 10 minutes
            if not lock.is_locked:
                lock.lock(timeout=datetime.timedelta(milliseconds=350))
                if os.path.isfile(f):  # the original file could be deleted in the meantime
                    return f, lock
                if lock.is_locked:
                    lock.unlock()
        except (AlreadyLockedError, TimeOutError):
            # some other process is analyzing the file; go ahead and look for another file
            pass
    return None, None


def analyze_strings(mystrings):
    """
    A list of mystrings gets  classified and only the predicted API keys are returned

    :param mystrings: a list of mystrings to be analyzed
    :return: a list of valid api keys
    :rtype: list
    """
    # for performance it's better to create a new list instead of removing elements from list
    smali_strings_filtered = []
    strings_features = []
    for string in mystrings:
        features = string_classifier.calculate_all_features(string.value)
        if features:
            features_list = list(features)
            smali_strings_filtered.append(string)
            strings_features.append(features_list)
    if len(strings_features) > 0:
        prediction = classifier.predict(np.array(strings_features))
        api_keys_strings = itertools.compress(smali_strings_filtered, prediction)  # basically a bitmask
        return api_keys_strings
    return []


def extract_metadata_resource(manifest_parser):
    metadata = manifest_parser.get_metadata()
    metadata_resources = []
    for m in metadata:
        if s_filter.pre_filter(m[1]):
            metadata_resources.append(ResourceString(ResourceString.TYPE_METADATA, m[0], m[1]))
    return metadata_resources


def extract_strings_resource(decoded_apk_folder):
    """
    Extracts all Android's string resources from a decoded apk

    :param decoded_apk_folder: folder that contains the decoded apk
    :return: a list of resource strings
    :rtype: list of ResourceString
    """
    strings_path = os.path.join(decoded_apk_folder, "res", "values", "strings.xml")
    if not os.path.exists(strings_path):
        logging.error("Strings resource file not found in {0}".format(decoded_apk_folder))
        return []
    strings_parser = AndroidStringsXmlParser(strings_path)
    resource_strings = strings_parser.get_string_resources(s_filter.pre_filter_mystring)
    resources_filtered = []
    for resource in resource_strings:
        if s_filter.pre_filter_mystring(resource):
            resources_filtered.append(resource)
    return resources_filtered


def extract_smali_strings(decoded_apk_folder, package, manifest_parser):
    """
    Extracts the strings contained in the smali files from a decoded apk

    :param decoded_apk_folder: folder that contains the decoded apk
    :param package: name of the app (e.g. com.example.myapp)
    :param manifest_parser: initialized instance of AndroidManifestXmlParser containing the application's Manifest
    :return: a list of strings
    :rtype: list of SmaliString
    """
    main_activity = manifest_parser.get_main_activity_name()
    if not main_activity:
        logging.error("Unable to find Main Activity. Using package name to find smali source")
        main_activity = package
    package_pieces = main_activity.split(".")[:-1]
    package_pieces = package_pieces[:2]
    # if, for example, we have a package named 'com.team.example', to avoid looking in countless library files,
    # we must search for smali files in paths like:
    #
    #     smali/com/team/example/randomfolder/a.smali
    #     smali_classes6/com/team/anotherparent/childfolder/test.smali
    #     smali_classes2/com/team/X/0eb.smali
    #
    # and so on. So we use a path with wildcards like this:
    #
    #     smali*/com/team/**/*.smali
    #
    # Note that we don't consider the last part of the package, because
    # a lot of developers use this folders structure:
    # app name: com.team.example
    #     com.team.example.MainActivity.class
    #     com.team.myutilities.Tool.class
    #     com.team.api.server.Model.class
    #     ...
    source_path = os.path.join(decoded_apk_folder, "smali*")
    for piece in package_pieces:
        source_path = os.path.join(source_path, piece)
    source_path = os.path.join(source_path, '**')
    source_path = os.path.join(source_path, '*.smali')

    smali_strings = []
    source_identified = False
    for filename in glob.iglob(source_path, recursive=True):
        source_identified = True
        parser = SmaliParser(filename)
        smalis = parser.get_strings()
        smalis_filtered = []
        for smali_string in smalis:
            if s_filter.pre_filter_mystring(smali_string):
                smalis_filtered.append(smali_string)
        smali_strings += smalis_filtered
    if not source_identified:
        logging.error("Unable to determine source folder in {0}".format(package))
        return []
    return smali_strings


def extract_native_strings(decoded_apk_folder):
    """
    Extract the strings contained in the native libraries found in a decoded apk

    :param decoded_apk_folder: folder that contains the decoded apk
    :return: a list of strings
    :rtype: list of LibString
    """
    lib_strings = set()
    lib_path = os.path.join(decoded_apk_folder, "lib")
    if os.path.exists(lib_path):
        path_to_be_inspected = None
        arc_priority_list = ["armeabi", "armeabi-v7a", "arm64-v8a", "x86", "x86_64", "mips", "mips64"]
        for arc in arc_priority_list:
            if os.path.exists(os.path.join(lib_path, arc)):
                path_to_be_inspected = os.path.join(lib_path, arc)
                break
        if path_to_be_inspected:
            for filename in glob.iglob(path_to_be_inspected + '/**/*.so', recursive=True):
                logging.debug("Found shared object lib: {0}".format(filename))
                base_filename = os.path.basename(filename)
                if base_filename in lib_blacklist:
                    # if the library is a generic one, we can safely ignore it
                    # since it would probably not contain any interesting information
                    continue
                try:
                    for string in strings(filename, conf.shared_object_sections, 4):
                        lib_string = LibString(base_filename, string)
                        if s_filter.pre_filter_mystring(lib_string):
                            lib_strings.add(lib_string)
                except (ELFError, ValueError) as e:
                    logging.error(str(e))
    return lib_strings


def analyze_decoded_apk(decoded_apk_folder):
    """
    Given a decoded apk (e.g. decoded using apktool), analyzes its content to extract API keys

    :param decoded_apk_folder: folder that contains the decoded apk
    :return: a list of api keys found, the name of the package, the version code and the version name
    """
    manifest = os.path.join(decoded_apk_folder, "AndroidManifest.xml")
    if not os.path.exists(manifest):
        logging.error("Unable to find manifest file for {0}".format(decoded_apk_folder))
        return
    manifest_parser = AndroidManifestXmlParser(manifest)
    package = manifest_parser.get_package()
    if not package:
        logging.error("Unable to determine package name for {0}".format(decoded_apk_folder))
        return
    version_code = 0
    version_name = "0"
    yml_file = os.path.join(decoded_apk_folder, "apktool.yml")
    if not os.path.exists(yml_file):
        logging.warning("Unable to find apktool.yml file for {0}".format(decoded_apk_folder))
    else:
        try:
            yml_parser = ApktoolYmlParser(yml_file)
            version_code = int(yml_parser.get_version_code())
            version_name = yml_parser.get_version_name()
        except (IOError, ValueError) as e:
            logging.error("Unable to parse apktool.yml; {0}".format(e))
    extracted = extract_metadata_resource(manifest_parser)
    extracted += extract_strings_resource(decoded_apk_folder)
    extracted += extract_smali_strings(decoded_apk_folder, package, manifest_parser)
    extracted += extract_native_strings(decoded_apk_folder)
    apikey_strings = analyze_strings(extracted)
    apikey_postfiltered = []
    for mystring in apikey_strings:
        if s_filter.post_filter_mystring(mystring):
            apikey_postfiltered.append(mystring)
    return apikey_postfiltered, package, version_code, version_name


def decode_apk(apk_path, output_path, apktool_path):
    """
    Decodes an apk using the external apktool tool

    :param apk_path: path of the apk to be decoded
    :param output_path: decoded apk folder
    :param apktool_path: where apktool.jar resides
    """
    completed_process = subprocess.run(["java", "-jar", apktool_path, "d", apk_path, "-o", output_path, "-f"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if completed_process.stdout:
        logging.info('Apktool: \n{0}'.format(completed_process.stdout))
    if completed_process.stderr:
        logging.error('Apktool: \n{0}'.format(completed_process.stderr))
    completed_process.check_returncode()


def analyze_apk(apk_path, decoded_apk_output_path, apktool_path):
    """
    Given an apk, decodes it and analyzes its content to extract API keys

    :param apk_path: path of the apk to be analyzed
    :param decoded_apk_output_path: where the decoded apk should be placed
    :param apktool_path: where apktool.jar resides, used for apk decode
    """
    try:
        decode_apk(apk_path, decoded_apk_output_path, apktool_path)
        if os.path.exists(decoded_apk_output_path):
            return analyze_decoded_apk(decoded_apk_output_path)
        else:
            raise ApkAnalysisError("Unable to find decoded folder for {0}".format(apk_path))
    except subprocess.CalledProcessError as err:
        logging.error("Error in " + str(err.cmd))
        raise ApkAnalysisError(err.stderr)

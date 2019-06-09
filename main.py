#!/usr/bin/env python3
import argparse
import logging
import logging.config
import os
import shutil
import sys
import time
import json

from console_dump import ConsoleDump
from mongodb_dump import MongoDBDump
from json_dump import JsonDump

import config

LOG_CONFIG_PATH = "log_config.json"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Configure logging
with open(os.path.join(__location__, LOG_CONFIG_PATH), "r", encoding="utf-8") as fd:
    log_config = json.load(fd)
    logging.config.dictConfig(log_config["logging"])

import apk_analyzer


def clean_resources(apk_path, lock, decoded_apk_output_path, apks_analyzed_dir, remove_apk=False):
    """
    Clean the resources allocated to analyze a string

    :param apk_path: path of the apk that has been
    :param lock: a lock that is locking the aforementioned apk
    :param decoded_apk_output_path: where the decoded apk where placed
    :param apks_analyzed_dir: where the apk should be moved after analysis; None if it should not be moved
    :param remove_apk: True if the apk should be deleted; ignored if apks_analyzed_dir is not None
    """
    apk = os.path.basename(apk_path)
    try:
        if os.path.exists(decoded_apk_output_path):
            shutil.rmtree(decoded_apk_output_path)
        else:
            logging.error("Unable to find decoded folder for {0}".format(apk_path))
        if apks_analyzed_dir:
            if not os.path.exists(apks_analyzed_dir):
                os.mkdir(apks_analyzed_dir)
            # either way, move the apk out of apk dir
            shutil.move(apk_path, os.path.join(apks_analyzed_dir, apk))
        elif remove_apk:
            os.remove(apk_path)
    finally:
        if lock:
            # unlock and clean temp files; cleaning should not be necessary
            # noinspection PyProtectedMember
            lockfile = lock._lockfile
            if lock.is_locked:
                lock.unlock()
            if os.path.exists(lockfile):
                os.remove(lockfile)


def analyze_apk(apk_path, apks_decoded_dir, apks_analyzed_dir, apktool_path, lock=None):
    apk = os.path.basename(apk_path)
    decoded_output_path = os.path.join(apks_decoded_dir, apk)
    try:
        apikeys, all_strings, package, version_code, version_name = apk_analyzer.analyze_apk(apk_path, decoded_output_path,
                                                                                apktool_path)
        if apikeys:
            dump = None
            if config.dump_location == "console":
                dump = ConsoleDump()
            elif config.dump_location == "jsonlines":
                dump = JsonDump()
            elif config.dump_location == "mongodb":
                dump = MongoDBDump()
            else:
                print("Unrecognized dump location: {0}".format(config.dump_location))
                exit(1)
            dump.dump_apikeys(apikeys, package, version_code, version_name)
            if config.dump_all_strings:
                dump.dump_strings(all_strings)
    except apk_analyzer.ApkAnalysisError as e:
        logging.error(str(e))
    clean_resources(apk_path, lock, decoded_output_path, apks_analyzed_dir, not config.save_analyzed_apks)


def monitor_apks_folder(apks_dir, apks_decoded_dir, apks_analyzed_dir, apktool_path):
    logging.info("Monitoring {0} for apks...".format(apks_dir))
    try:
        while True:
            apk_path, lock = apk_analyzer.get_next_apk(apks_dir)
            if lock is not None:
                logging.info("Detected {0}".format(apk_path))
                analyze_apk(apk_path, apks_decoded_dir, apks_analyzed_dir, apktool_path, lock, True, False, True)
                logging.info("{0} analyzed".format(apk_path))
            else:
                time.sleep(1)

    except KeyboardInterrupt:
        print('\nInterrupted!')


def main():
    parser = argparse.ArgumentParser(
        description='A python program that finds API-KEYS and secrets hidden inside strings', add_help=True
    )
    parser.add_argument('--debug', action="store_true", dest='boolean_debug',
                        default=False, help='Print debug information')
    parser.add_argument('--analyze-apk', action='store', dest='apk_path',
                        help='Analyze a single apk to find hidden API Keys')
    parser.add_argument('--monitor-apks-folder', action="store_true", dest='boolean_monitor',
                        default=False, help='Monitors the configured apks folder for new apks. '
                                            'When a new apk is detected, the file is locked and analysis starts.')

    results = parser.parse_args()

    # functions that don't need gibberish detector

    if results.boolean_debug:
        logging.basicConfig(level=logging.DEBUG)
    elif results.apk_path:
        analyze_apk(results.apk_path, os.path.abspath(config.apks_decoded_dir),
                    None, os.path.abspath(config.apktool))
        return
    elif results.boolean_monitor:
        apks_analyzed_dir = None
        if config.save_analyzed_apks:
            apks_analyzed_dir = os.path.abspath(config.apks_analyzed_dir)
        monitor_apks_folder(os.path.abspath(config.apks_dir), os.path.abspath(config.apks_decoded_dir),
                            apks_analyzed_dir, os.path.abspath(config.apktool))
        return
    parser.print_help()


if __name__ == '__main__':
    main()

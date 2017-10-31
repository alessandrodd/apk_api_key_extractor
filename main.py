#!/usr/bin/env python3
import argparse
import logging
import os
import shutil
import sys
import time
from logging.config import dictConfig

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(1, os.path.join(__location__, "api-key-detector"))

from config import conf

dictConfig(conf.logging)
import db_interface
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


def analyze_apk(apk_path, apks_decoded_dir, apks_analyzed_dir, apktool_path, lock=None, dump=True, remove_apk=False):
    apk = os.path.basename(apk_path)
    decoded_output_path = os.path.join(apks_decoded_dir, apk)
    try:
        apikeys, package, version_code, version_name = apk_analyzer.analyze_apk(apk_path, decoded_output_path,
                                                                                apktool_path)
        if apikeys and dump:
            db_interface.dump(apikeys, package, version_code, version_name)
        elif apikeys and not dump:
            print(apikeys)
    except apk_analyzer.ApkAnalysisError as e:
        logging.error(str(e))
    clean_resources(apk_path, lock, decoded_output_path, apks_analyzed_dir, remove_apk)


def monitor_apks_folder(apks_dir, apks_decoded_dir, apks_analyzed_dir, apktool_path):
    logging.info("Monitoring {0} for apks...".format(apks_dir))
    try:
        while True:
            apk_path, lock = apk_analyzer.get_next_apk(apks_dir)
            if lock is not None:
                logging.info("Detected {0}".format(apk_path))
                analyze_apk(apk_path, apks_decoded_dir, apks_analyzed_dir, apktool_path, lock, True, True)
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
        analyze_apk(results.apk_path, os.path.abspath(conf.apks_decoded),
                    None, os.path.abspath(conf.apktool), dump=False, remove_apk=False)
        return
    elif results.boolean_monitor:
        apks_analyzed = None
        if conf.save_analyzed_apks:
            apks_analyzed = os.path.abspath(conf.apks_analyzed)
        monitor_apks_folder(os.path.abspath(conf.apks_folder), os.path.abspath(conf.apks_decoded),
                            apks_analyzed, os.path.abspath(conf.apktool))
        return
    parser.print_help()


if __name__ == '__main__':
    main()

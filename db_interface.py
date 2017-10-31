import datetime
import json
import logging
import os

import pymongo
from flufl.lock import Lock, AlreadyLockedError, TimeOutError
from pymongo.errors import AutoReconnect
from retry_decorator import retry

from config import conf, dbconf

dest = conf.key_dump
dump = None
collection = None

LOCK_PREFIX = ".lock"
COLLECTION_NAME = "key_dump"


def dump_to_file(entries, package, version_code, version_name):
    lock_acquired = False
    while not lock_acquired:
        try:
            filename = dest + LOCK_PREFIX
            lock = Lock(filename, lifetime=datetime.timedelta(seconds=6000))  # expires in 10 minutes
            if not lock.is_locked:
                lock.lock(timeout=datetime.timedelta(milliseconds=350))
                lock_acquired = True
                with open(dest, 'a') as f:
                    first = True
                    if os.path.exists(dest) and os.path.getsize(dest) > 0:
                        first = False
                    for entry in entries:
                        entry_dict = entry.__dict__
                        entry_dict['package'] = package
                        entry_dict['versionCode'] = version_code
                        entry_dict['versionName'] = version_name
                        if first:
                            first = False
                        else:
                            f.write(",\n")
                        json.dump(entry_dict, f, indent=4)
                if lock.is_locked:
                    lock.unlock()
        except (AlreadyLockedError, TimeOutError):
            # some other process is analyzing the file; go ahead and look for another file
            pass


@retry(pymongo.errors.AutoReconnect, tries=5, timeout_secs=1)
def dump_to_mongodb(entries, package, version_code, version_name):
    # noinspection PyUnusedLocal
    entries_dicts = []
    for entry in entries:
        entry_dict = entry.__dict__
        entry_dict['package'] = package
        entry_dict['versionCode'] = version_code
        entry_dict['versionName'] = version_name
        entries_dicts.append(entry_dict)
    if entries_dicts:
        collection.insert_many(entries_dicts, False)


@retry(pymongo.errors.AutoReconnect, tries=5, timeout_secs=1)
def get_apikey_unverified():
    document = collection.find_one({"verified": None})
    return document


@retry(pymongo.errors.AutoReconnect, tries=5, timeout_secs=1)
def set_apikey_verified(api_id):
    document_before = collection.find_one_and_update({'_id': api_id}, {"$set": {"verified": True}})
    if not document_before:
        logging.error("Unable to set api {0} as verified! Id not found.".format(api_id))


@retry(pymongo.errors.AutoReconnect, tries=5, timeout_secs=1)
def remove_apikey(api_id):
    collection.remove(api_id)


# check if it's an HTTP address or local path
if dest == 'remote':
    # remote dump location
    client = pymongo.MongoClient(dbconf.address, int(dbconf.port), username=dbconf.user, password=dbconf.password)
    db = client[dbconf.name]
    collection = db[COLLECTION_NAME]
    dump = dump_to_mongodb

elif dest == 'local':
    dest = os.path.abspath(conf.local_dump_file)
    dump = dump_to_file
else:
    logging.error("INVALID destination type: {0} (expected remote or local)".format(dest))

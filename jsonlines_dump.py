import datetime
import json
import logging
import os

from flufl.lock import Lock, AlreadyLockedError, TimeOutError

from abstract_dump import AbstractDump

import config

LOCK_PREFIX = ".lock"


class JsonlinesDump(AbstractDump):

    def __init__(self):
        self.dest = os.path.abspath(config.jsonlines["dump_file"])
        self.strings_dest = os.path.abspath(config.jsonlines["strings_file"])

    def dump_apikeys(self, entries, package, version_code, version_name):
        lock_acquired = False
        while not lock_acquired:
            try:
                filename = self.dest + LOCK_PREFIX
                lock = Lock(filename, lifetime=datetime.timedelta(seconds=6000))  # expires in 10 minutes
                if not lock.is_locked:
                    lock.lock(timeout=datetime.timedelta(milliseconds=350))
                    lock_acquired = True
                    with open(self.dest, 'a') as f:
                        first = True
                        if os.path.exists(self.dest) and os.path.getsize(self.dest) > 0:
                            first = False
                        for entry in entries:
                            entry_dict = entry.__dict__
                            entry_dict['package'] = package
                            entry_dict['versionCode'] = version_code
                            entry_dict['versionName'] = version_name
                            if first:
                                first = False
                            else:
                                f.write("\n")
                            json.dump(entry_dict, f)
                    if lock.is_locked:
                        lock.unlock()
            except (AlreadyLockedError, TimeOutError):
                # some other process is analyzing the file; go ahead and look for another file
                pass

    def dump_strings(self, entries):
        lock_acquired = False
        while not lock_acquired:
            try:
                filename = self.strings_dest + LOCK_PREFIX
                lock = Lock(filename, lifetime=datetime.timedelta(seconds=6000))  # expires in 10 minutes
                if not lock.is_locked:
                    lock.lock(timeout=datetime.timedelta(milliseconds=350))
                    lock_acquired = True
                    with open(self.strings_dest, 'a') as f:
                        first = True
                        if os.path.exists(self.strings_dest) and os.path.getsize(self.strings_dest) > 0:
                            first = False
                        for entry in entries:
                            entry_dict = entry.__dict__
                            if first:
                                first = False
                            else:
                                f.write("\n")
                            json.dump(entry_dict, f)
                    if lock.is_locked:
                        lock.unlock()
            except (AlreadyLockedError, TimeOutError):
                # some other process is analyzing the file; go ahead and look for another file
                pass

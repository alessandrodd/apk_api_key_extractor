import datetime
import json
import logging
import os

from abstract_dump import AbstractDump


class ConsoleDump(AbstractDump):

    def __init__(self):
        pass

    def dump_apikeys(self, entries, package, version_code, version_name):
        for entry in entries:
            entry_dict = entry.__dict__
            entry_dict['package'] = package
            entry_dict['versionCode'] = version_code
            entry_dict['versionName'] = version_name
            print(entry_dict)

    def dump_strings(self, entries):
        for entry in entries:
            entry_dict = entry.__dict__
            print(entry_dict)

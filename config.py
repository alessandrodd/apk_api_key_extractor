"""
Singleton implementation for config objects
"""
import logging
import os

from my_tools import config_parser

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

CONFIG_PATH = "config.json"
DB_CONFIG_PATH = "dbconfig.json"

conf = config_parser.parse(os.path.join(__location__, CONFIG_PATH))
dbconf = None
try:
    dbconf = config_parser.parse(os.path.join(__location__, DB_CONFIG_PATH))
except FileNotFoundError:
    logging.warning("Missing database configuration ({0})".format(DB_CONFIG_PATH))

import sys
import json


class Config(object):
    """
    A wrapper for json configuration files. Turns a json file into a
    python dictionary
    """
    def __init__(self, config):
        self.__dict__ = config

    def __str__(self):
        return str(self.__dict__)


def parse(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
    return Config(config)


def main(argv):
    if len(argv) != 2:
        print("Usage: python {0} config_file.json".format(argv[0]))
        return
    conf = parse(argv[1])
    print(str(conf))


if __name__ == '__main__':
    main(sys.argv)

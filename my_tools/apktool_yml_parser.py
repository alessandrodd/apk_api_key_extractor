import yaml


class ApktoolYmlParser(object):
    """
    Parser utility for apktool's apktool.yml file
    """

    def __init__(self, yml_file):
        """
        constructor for ApktoolYmlParser object

        :param yml_file: path of the apktool's apktool.yml file to be parsed
        """
        with open(yml_file, 'r') as f:
            # ignore yaml class tag
            # e.g. !!brut.androlib.meta.MetaInfo
            line = f.readline()
            if not line.startswith("!!"):
                f.seek(0)
            self.doc = yaml.safe_load(f)

    def get_version_code(self):
        return self.doc['versionInfo']['versionCode']

    def get_version_name(self):
        return self.doc['versionInfo']['versionName']

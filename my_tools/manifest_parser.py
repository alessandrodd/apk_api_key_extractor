from lxml import etree


class AndroidManifestXmlParser(object):
    """
    Parser utility for Android's AndroidManifest.xml file
    """

    def __init__(self, xml_file):
        """
        constructor for AndroidManifestXmlParser object

        :param xml_file: path of the Android's manifest (AndroidManifest.xml) file to be parsed
        """
        path = xml_file
        self.root = etree.parse(path, etree.XMLParser(encoding='utf-8', recover=True)).getroot()

    def get_package(self):
        return self.root.get("package")

    def get_metadata(self):
        metadata_rows = self.root.findall('.//meta-data')
        metadata = []
        for row in metadata_rows:
            name = row.get("{" + str(self.root.nsmap.get("android")) + "}name")
            value = row.get("{" + str(self.root.nsmap.get("android")) + "}value")
            if name and value:
                metadata.append((name, value))
        return metadata

    def get_activities(self):
        activities_rows = self.root.findall('.//activity')
        activities = []
        for row in activities_rows:
            activities.append(row.get("{" + str(self.root.nsmap.get("android")) + "}name"))
        return activities

    def get_activities_aliases(self):
        aliases_rows = self.root.findall('.//activity-alias')
        aliases = []
        for row in aliases_rows:
            aliases.append((row.get("{" + str(self.root.nsmap.get("android")) + "}name"),
                            row.get("{" + str(self.root.nsmap.get("android")) + "}targetActivity")))
        return aliases

    def get_main_activity_name(self):
        activities_rows = self.root.findall('.//activity')
        for row in activities_rows:
            action_rows = row.findall('.//action')
            for action_row in action_rows:
                if action_row.get("{" + str(self.root.nsmap.get("android")) + "}name") == "android.intent.action.MAIN":
                    activity_name = row.get("{" + str(self.root.nsmap.get("android")) + "}name")
                    if activity_name.startswith("."):
                        return self.get_package() + activity_name
                    elif "." not in activity_name:
                        return self.get_package() + "." + activity_name
                    return activity_name
        aliases_rows = self.root.findall('.//activity-alias')
        for row in aliases_rows:
            action_rows = row.findall('.//action')
            for action_row in action_rows:
                if action_row.get("{" + str(self.root.nsmap.get("android")) + "}name") == "android.intent.action.MAIN":
                    activity_name = row.get("{" + str(self.root.nsmap.get("android")) + "}targetActivity")
                    if activity_name.startswith("."):
                        return self.get_package() + activity_name
                    elif "." not in activity_name:
                        return self.get_package() + "." + activity_name
                    return activity_name
        return None

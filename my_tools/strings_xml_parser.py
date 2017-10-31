import sys

from lxml import etree

from my_model.resource_string import ResourceString


class AndroidStringsXmlParser(object):
    """
    Parser utility for Android's strings.xml file
    """

    def __init__(self, xml_file):
        """
        constructor for AndroidXmlParser object

        :param xml_file: path of the Android's string resource (strings.xml) file to be parsed
        """
        path = xml_file
        self.root = etree.parse(path, etree.XMLParser(encoding='utf-8', recover=True)).getroot()

    def get_all_elements(self):
        return list(self.root.iter())

    def get_string_resources(self, value_filter=None):
        """
        Gets all string and string-array elements from Android's strings.xml resource files

        Example:

            resources = test_instance.get_all_string_resources()

            for res in resources:
                print("{0} {1} {2}".format(res.row_type, res.name, res.value))

        :return: a list of ResourceString object.
        :rtype: list
        """
        resources = []
        for element in self.root.findall("string"):
            resource = ResourceString(ResourceString.TYPE_STRING, element.get("name"), element.text)
            if value_filter is None or value_filter(resource):
                resources.append(resource)

        for element in self.root.findall("string-array"):
            array_name = element.get("name")
            for item in element.findall("item"):
                resource = ResourceString(ResourceString.TYPE_ARRAY_ELEMENT, array_name, item.text)
                if value_filter is None or value_filter(resource):
                    resources.append(resource)
        return resources


def main(argv):
    if len(argv) != 2 and len(argv) != 3:
        print("Usage: python {0} path/xml/file.xml [substring_to_find]".format(argv[0]))
        return
    test_instance = AndroidStringsXmlParser(argv[1])
    if len(argv) == 2:
        resources = test_instance.get_string_resources()
    else:
        def value_filter(s):
            if argv[2] in s:
                return True
            return False

        resources = test_instance.get_string_resources(value_filter)
    for res in resources:
        print(res.name)
        print(res.value.decode('utf-8'))
        # print("{0} {1} {2}".format(res.row_type, res.name, res.value))


if __name__ == '__main__':
    main(sys.argv)

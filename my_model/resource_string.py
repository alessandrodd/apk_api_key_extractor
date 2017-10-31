from my_model.my_string import MyString


class ResourceString(MyString):
    """
    An interesting string that has been found in an Android's resource file
    """
    TYPE_STRING = "TYPE_RESOURCE_STRING"
    TYPE_ARRAY_ELEMENT = "TYPE_RESOURCE_ARRAY_ELEMENT"
    TYPE_METADATA = "TYPE_RESOURCE_METADATA"

    def __init__(self, row_type, name, value):
        super().__init__(name, value, row_type)

    def __str__(self):
        return super(ResourceString, self).__str__()

    def __repr__(self):
        return self.__str__()

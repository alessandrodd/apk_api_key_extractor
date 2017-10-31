class MyString(object):
    """
    An object representing an interesting string
    """
    TYPE_UNKNOWN = "TYPE_UNKNOWN"

    def __init__(self, name, value, source=TYPE_UNKNOWN):
        self.name = name
        self.value = value
        self.source = source

    def __str__(self):
        return "{0} {1} {2}".format(self.name, self.value, self.source)

    def __repr__(self):
        return self.__str__()

from my_model.my_string import MyString


class LibString(MyString):
    """
    String found with Unix's strings utility
    """
    TYPE_LIB = "TYPE_LIB_STRING"

    def __init__(self, name, value):
        super().__init__(name, value, LibString.TYPE_LIB)

    def __str__(self):
        return super(LibString, self).__str__()

    def __repr__(self):
        return self.__str__()

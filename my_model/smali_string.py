from my_model.my_string import MyString


class SmaliString(MyString):
    """
    An interesting string that has been found inside a smali code
    """
    TYPE_LOCAL_VAR = "TYPE_LOCAL_VAR"
    TYPE_INSTANCE_VAR = "TYPE_INSTANCE_VAR"
    TYPE_STATIC_VAR = "TYPE_STATIC_VAR"
    TYPE_METHOD_PARAMETER = "TYPE_METHOD_PARAMETER"

    def __init__(self, string_type, class_name, method_name, var_name, value, in_array=False, parameter_of=None):
        super().__init__(var_name, value, string_type)
        self.class_name = class_name
        self.method_name = method_name
        self.in_array = in_array
        self.parameter_of = parameter_of

    def __str__(self):
        s = super(SmaliString, self).__str__()
        s += " {0} {1}".format(self.class_name, self.method_name)
        if self.in_array:
            s += " In Array: {0}".format(self.in_array)
        if self.parameter_of:
            s += " Parameter of: {0}".format(self.parameter_of)
        return s

    def __repr__(self):
        return self.__str__()

import codecs
import logging
import re
import sys

from my_model.smali_string import SmaliString


class SmaliParser(object):
    """
    A quick and dirty, partial parser for Smali code.
    Made for the apk-apikey-grabber project and probably not suitable for other tasks.
    The objective of this code is to retrieve as much information as possible about
    String variables while avoiding implementing an entire Smali parser. The complete set of smali
    operations is quite big, here just a subset of these operations was considered, so
    it will NOT be 100% accurate, especially when trying to parse arrays of strings or method parameters.
    """

    def __init__(self, smali_file):
        """
        constructor for SmaliParser object

        For information about dalvik opcodes see here:
        http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html

        :param smali_file: path of the smali file to be parsed
        """
        self._smali_file = smali_file

    def get_strings(self):
        strings = []
        with codecs.open(self._smali_file, 'r', encoding='utf8') as f:
            current_class = None
            current_method = None
            current_const_string = None
            # indicates how many elements (starting from the last element f the list)
            # are part of the array currently being parsed
            # e.g. 3 means that the latest 3 elements in the 'strings' list are part of the same array
            # that is still being parsed
            current_array_reverse_index = 0
            current_call_index = 0

            for l in f.readlines():
                l = l.lstrip()

                if not l:
                    continue

                if not l.startswith(('.line', '.local', 'iput-object', 'sput-object', 'invoke')):
                    current_const_string = None
                    if not l.startswith(('const/4', 'const-string', 'aput-object', 'new-array', 'fill-array-data')):
                        current_array_reverse_index = 0

                if l.startswith('.class'):
                    match_class = is_class(l)
                    if match_class:
                        current_class = extract_class(match_class)

                elif l.startswith('.field'):
                    match_class_property = is_class_property(l)
                    if match_class_property:
                        field = extract_class_property(match_class_property)
                        if not field:
                            logging.warning("Unable to extract class property from " + l)
                        elif field['value'] and field['value'] != 'null':  # we don't want empty strings or variables
                            if not current_class:
                                logging.warning("Cannot retrieve class information for local var! String: {0}".format(
                                    current_const_string))
                                cls = ""
                            else:
                                cls = current_class['name']
                            smali_string = SmaliString(SmaliString.TYPE_STATIC_VAR, cls, "", field['property_name'],
                                                       field['value'])
                            strings.append(smali_string)
                        current_const_string = None
                        current_array_reverse_index = 0

                elif l.startswith('const-string'):
                    match_const_string = is_const_string_jumbo(l)
                    if not match_const_string:
                        match_const_string = is_const_string(l)
                    if match_const_string:
                        current_const_string = extract_const_string(match_const_string)
                        if type(current_const_string) == list:
                            for c in current_const_string:
                                current_array_reverse_index += 1
                                push_smali_string(strings, current_class, current_method, c)
                                strings[-1].in_array = True
                            current_const_string = None
                        elif not current_const_string:
                            logging.warning("Unable to extract current const string from " + l)
                        else:
                            push_smali_string(strings, current_class, current_method, current_const_string)
                    else:
                        logging.warning("unmatchable const-string: {0}".format(l))

                elif l.startswith('.method'):
                    match_class_method = is_class_method(l)
                    if match_class_method:
                        m = extract_class_method(match_class_method)
                        if not m:
                            logging.warning("Unable to extract class method from " + l)
                        else:
                            current_method = m
                        current_call_index = 0

                elif l.startswith('invoke'):
                    match_method_call = is_method_call(l)
                    if match_method_call:
                        m = extract_method_call(match_method_call)
                        if not m:
                            logging.warning("Unable to extract method call from " + l)
                        else:
                            # Add calling method (src)
                            m['src'] = current_method['name']

                            # Add call index
                            m['index'] = current_call_index
                            current_call_index += 1

                            if current_const_string and not current_array_reverse_index:
                                strings[-1].parameter_of = m['to_class'] + "." + m['to_method']
                                strings[-1].string_type = SmaliString.TYPE_METHOD_PARAMETER
                            elif not current_const_string and current_array_reverse_index and len(strings) > 0:
                                end_index = max(-1, len(strings) - current_array_reverse_index - 1)
                                for i in range(len(strings) - 1, end_index, -1):
                                    strings[i].parameter_of = m['to_class'] + "." + m['to_method']
                                    strings[i].string_type = SmaliString.TYPE_METHOD_PARAMETER
                            current_const_string = None
                            current_array_reverse_index = 0

                elif l.startswith('aput-object'):
                    match_aput_object = is_aput_object(l)
                    if match_aput_object:
                        aput_info = extract_aput_object(match_aput_object)
                        if not aput_info:
                            logging.warning("Unable to extract aput object from " + l)
                        elif strings and strings[-1].name == aput_info['reference']:
                            strings[-1].in_array = True
                            current_array_reverse_index += 1
                            current_const_string = None
                        else:
                            current_array_reverse_index = 0

                elif l.startswith('iput-object'):
                    match_iput_object = is_iput_object(l)
                    if match_iput_object:
                        iput_info = extract_iput_object(match_iput_object)
                        if not iput_info:
                            logging.warning("Unable to extract iput object from " + l)
                        elif current_const_string and not current_array_reverse_index:
                            strings[-1].name = iput_info['variable_name']
                            strings[-1].string_type = SmaliString.TYPE_INSTANCE_VAR
                        elif not current_const_string and current_array_reverse_index and len(strings) > 0:
                            end_index = max(-1, len(strings) - current_array_reverse_index - 1)
                            for i in range(len(strings) - 1, end_index, -1):
                                strings[i].name = iput_info['variable_name']
                                strings[i].string_type = SmaliString.TYPE_INSTANCE_VAR
                        else:
                            pass
                            # logging.warning("Encountered iput-object in an unexpected position in line " + l)
                        current_const_string = None
                        current_array_reverse_index = 0

                elif l.startswith('sput-object'):
                    match_sput_object = is_sput_object(l)
                    if match_sput_object:
                        sput_info = extract_sput_object(match_sput_object)
                        if not sput_info:
                            logging.warning("Unable to extract spunt object from " + l)
                        elif current_const_string and not current_array_reverse_index:
                            strings[-1].name = sput_info['variable_name']
                            strings[-1].string_type = SmaliString.TYPE_STATIC_VAR
                        elif not current_const_string and current_array_reverse_index and len(strings) > 0:
                            end_index = max(-1, len(strings) - current_array_reverse_index - 1)
                            for i in range(len(strings) - 1, end_index, -1):
                                strings[i].name = sput_info['variable_name']
                                strings[i].string_type = SmaliString.TYPE_STATIC_VAR
                        else:
                            pass
                            # logging.warning("Encountered sput-object in an unexpected position in line " + l)
                        current_const_string = None
                        current_array_reverse_index = 0

                elif l.startswith('.local'):
                    match_local = is_local_debug_info(l)
                    if match_local:
                        local_debug_info = extract_local_debug_info(match_local)
                        if not local_debug_info:
                            logging.warning("Unable to extract local debug info from " + l)
                        elif current_const_string and not current_array_reverse_index:
                            strings[-1].name = local_debug_info['variable_name']
                        elif not current_const_string and current_array_reverse_index and len(strings) > 0:
                            end_index = max(-1, len(strings) - current_array_reverse_index - 1)
                            for i in range(len(strings) - 1, end_index, -1):
                                strings[i].name = local_debug_info['variable_name']
                        else:
                            pass
                            # logging.warning("Encountered .local in an unexpected position in line " + l)
                        current_const_string = None
                        current_array_reverse_index = 0

        f.close()
        return strings


def push_smali_string(strings, current_class, current_method, current_const_string):
    """
    Adds a SmaliString resource to the strings list with as much information as possible

    :param strings: SmaliString list
    :param current_class: the class that is being parsed or None
    :param current_method: the method that is being parsed or None
    :param current_const_string: the string that is being parsed
    :return:True if an element was added, False otherwise
    :rtype: bool
    """
    if not current_const_string:
        logging.debug("false")
        return False

    if not current_class:
        logging.warning("Cannot retrieve class information for local var! String: {0}".format(current_const_string))
        cls = ""
    else:
        cls = current_class['name']

    if not current_method:
        logging.warning(
            "Cannot retrieve method information for local var! String: {0}".format(current_const_string))
        mthd = ""
    else:
        mthd = current_method['name']

    var_name = current_const_string['name']

    smali_string = SmaliString(SmaliString.TYPE_LOCAL_VAR, cls, mthd, var_name, current_const_string['value'])
    strings.append(smali_string)
    return True


# thanks to 0rka for regex patterns
# https://0rka.blog/2017/07/04/dalviks-smali-static-code-analysis-with-python/
regex_class_name = re.compile(r"^\.class.*\ (.+(?=\;))", re.MULTILINE)
regex_method_data = re.compile(r'^\.method.+?\ (.+?(?=\())\((.*?)\)(.*?$)(.*?(?=\.end\ method))',
                               re.MULTILINE | re.DOTALL)
regex_called_methods = re.compile(
    r'invoke-.*?\ {(.*?)}, (.+?(?=;))\;\-\>(.+?(?=\())\((.*?)\)(.*?)(?=$|;)', re.MULTILINE | re.DOTALL)
regex_move_result = re.compile(r'move-result.+?(.*?)$', re.MULTILINE | re.DOTALL)
regex_class = re.compile("\.class\s+(?P<class>.*);")
regex_property = re.compile("\.field\s+(?P<property>.*)")
regex_const_string = re.compile("const-string\s+(?P<const>.*)")
regex_const_string_jumbo = re.compile("const-string/jumbo\s+(?P<const>.*)")
regex_method = re.compile("\.method\s+(?P<method>.*)$")
regex_invoke = re.compile("invoke-\w+(?P<invoke>.*)")
regex_aput_object = re.compile("aput-object\s+(?P<aput>.*)")
regex_ipub_object = re.compile("iput-object\s+(?P<iput>.*)")
regex_sput_object = re.compile("sput-object\s+(?P<sput>.*)")
regex_local = re.compile(".local\s+(?P<local>.*)")
regex_extract_class = re.compile('(?P<name>[^:]*):(?P<type>[^(;|\s)]*)(;|\s)*(?P<dirtyvalue>.*)')
regex_value = re.compile('\s*=\s+(?P<value>.*)')
regex_var = re.compile('(?P<var>.*),\s+"(?P<value>.*)"')
regex_class_method = re.compile("(?P<name>.*)\((?P<args>.*)\)(?P<return>.*)")
regex_method_call = re.compile('(?P<local_args>\{.*\}),\s+(?P<dst_class>.*);->'
                               '(?P<dst_method>.*)\((?P<dst_args>.*)\)(?P<return>.*)')
regex_extract_aput_object = re.compile('(?P<reference>.*),\s+(?P<array>.*),\s+(?P<index>.*)')
regex_extract_iput_object = re.compile('(?P<ref>.*),\s+(?P<instance>.*),\s+(?P<pkg>[^;]*);*->'
                                       '(?P<name>[^:]*):(?P<type>[^;]*);*')
regex_extract_sput_object = re.compile('(?P<ref>.*),\s+(?P<pkg>[^;]*);*->(?P<name>[^:]*):(?P<type>[^;]*);*')
regex_extract_local = re.compile('(?P<var>.*),\s+"(?P<name>.*)":(?P<type>[^;]*);*(?P<signature>.*)')


def is_class(line):
    """Check if line contains a class definition

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains class informations or None
    :rtype: str
    """
    match = regex_class.search(line)
    if match:
        logging.debug("Found class: %s" % match.group('class'))
        return match.group('class')
    else:
        return None


def is_class_property(line):
    """Check if line contains a field definition

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains class property information or None
    :rtype: str
    """
    match = regex_property.search(line)
    if match:
        logging.debug("Found property: %s" % match.group('property'))
        return match.group('property')
    else:
        return None


def is_const_string(line):
    """Check if line contains a const-string

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains const-string information or None
    :rtype: str
    """
    match = regex_const_string.search(line)
    if match:
        logging.debug("Found const-string: %s" % match.group('const'))
        return match.group('const')
    else:
        return None


def is_const_string_jumbo(line):
    """Check if line contains a const-string/jumbo

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains const-string information or None
    :rtype: str
    """
    match = regex_const_string_jumbo.search(line)
    if match:
        logging.debug("Found const-string/jumbo: %s" % match.group('const'))
        return match.group('const')
    else:
        return None


def is_class_method(line):
    """Check if line contains a method definition

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains method information or None
    :rtype: str
    """
    match = regex_method.search(line)
    if match:
        logging.debug("Found method: %s" % match.group('method'))
        return match.group('method')
    else:
        return None


def is_method_call(line):
    """Check [if the line contains a method call (invoke-*)

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains call information or None
    :rtype: str
    """
    match = regex_invoke.search(line)
    if match:
        logging.debug("Found invoke: %s" % match.group('invoke'))
        return match.group('invoke')
    else:
        return None


def is_aput_object(line):
    """Check if line contains an aput-object command

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains aput-object or None
    :rtype: str
    """
    match = regex_aput_object.search(line)
    if match:
        logging.debug("Found aput-object: %s" % match.group('aput'))
        return match.group('aput')
    else:
        return None


def is_iput_object(line):
    """Check if line contains an iput-object command

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains iput-object or None
    :rtype: str
    """
    match = regex_ipub_object.search(line)
    if match:
        logging.debug("Found iput-object: %s" % match.group('iput'))
        return match.group('iput')
    else:
        return None


def is_sput_object(line):
    """Check if line contains an sput-object command

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains sput-object or None
    :rtype: str
    """
    match = regex_sput_object.search(line)
    if match:
        logging.debug("Found sput-object: %s" % match.group('sput'))
        return match.group('sput')
    else:
        return None


def is_local_debug_info(line):
    """Check if line contains a local debug information

    :line: Text line to be checked

    :return: A one-element Tuple (basically a string) that contains debug information or None
    :rtype: str
    """
    match = regex_local.search(line)
    if match:
        logging.debug("Found local debug info: %s" % match.group('local'))
        return match.group('local')
    else:
        return None


def extract_class(data):
    """Extract class information from a string

    :data: Data would be sth like: public static Lcom/a/b/c

    :return: Returns a class object, otherwise None
    :rtype: dict
    """
    class_info = data.split(" ")
    logging.debug("class_info: %s" % class_info[-1].split('/')[:-1])
    c = {
        # Last element is the class name
        'name': class_info[-1],

        # Package name
        'package': ".".join(class_info[-1].split('/')[:-1]),

        # Class deepth
        'depth': len(class_info[-1].split("/")),

        # All elements refer to the type of class
        'type': " ".join(class_info[:-1]),

        # Properties
        'properties': [],

        # Const strings
        'const-strings': [],

        # Methods
        'methods': []
    }

    return c


def extract_class_property(data):
    """Extract class property information from a string

    :data: Data would be sth like: private cacheSize:I

    :return: Returns a property object, otherwise None
    :rtype: dict
    """

    match = regex_extract_class.search(data)

    if match:
        # A field/property is usually saved in this form
        #  <modifiers> <name>:<type>
        # or
        # <modifiers> <name>:<type>; = <value>

        dirty_value = match.group('dirtyvalue')
        value = ""

        if dirty_value:
            match2 = regex_value.search(dirty_value)
            if not match2:
                logging.warning("Unable to parse value for " + dirty_value)
            else:
                value = match2.group('value')
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

        modifiers = []
        name = None
        name_modifiers = match.group('name')
        name_modifiers_splitted = name_modifiers.split(" ")
        for i in range(len(name_modifiers_splitted)):
            if i == len(name_modifiers_splitted) - 1:
                name = name_modifiers_splitted[i]
            else:
                modifiers.append(name_modifiers_splitted[i])
        p = {
            # modifiers
            'modifiers': modifiers,

            # Property name
            'property_name': name,

            # Property type
            'type': match.group('type') if len(match.group('type')) > 1 else '',

            # Value
            'value': value
        }

        return p
    else:
        return None


def extract_const_string(data):
    """Extract const string information from a string

    Warning: strings array seems to be practically indistinguishable from strings with ", ".
    e.g.

    The following is an array of two elements

    const/4 v0, 0x1
    new-array v0, v0, [Ljava/lang/String;
    const/4 v1, 0x0
    const-string v2, "NIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4, OIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"
    aput-object v2, v0, v1

    It seems equal to this other case:

    const/4 v0, 0x2
    new-array v0, v0, [Ljava/lang/String;
    const/4 v1, 0x0
    const-string v2, "LIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4"
    aput-object v2, v0, v1

    But who says that in the second case the const-string last argument is just a string while in the
    first case the last arg are two elements of the array?

    :data: Data would be sth like: v0, "this is a string"

    :return: Returns a const string object, otherwise None
    :rtype: dict or list
    """
    match = regex_var.search(data)

    if match:
        # A const string is usually saved in this form
        #  <variable name>,<value>

        name = match.group('var')
        value = match.group('value')

        if ", " not in value:

            c = {
                # Variable
                'name': name,

                # Value of string
                'value': value
            }

            return c
        else:
            c = []
            for val in value.split(", "):
                c.append({
                    'name': name,

                    'value': val
                })
            return c
    else:
        return None


def extract_class_method(data):
    """Extract class method information from a string

    :data: Data would be sth like:
         public abstract isTrue(ILjava/lang/..;ILJava/string;)I

    :return: Returns a method object, otherwise None
    :rtype: dict
    """
    method_info = data.split(" ")

    # A method looks like:
    #  <name>(<arguments>)<return value>
    m_name = method_info[-1]
    m_args = None
    m_ret = None

    # Search for name, arguments and return value
    match = regex_class_method.search(method_info[-1])

    if match:
        m_name = match.group('name')
        m_args = match.group('args')
        m_ret = match.group('return')

    m = {
        # Method name
        'name': m_name,

        # Arguments
        'args': m_args,

        # Return value
        'return': m_ret,

        # Additional info such as public static etc.
        'type': " ".join(method_info[:-1]),

        # Calls
        'calls': []
    }

    return m


def extract_method_call(data):
    """Extract method call information from a string

    :data: Data would be sth like:
         {v0}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    :return: Returns a call object, otherwise None
    :rtype: dict
    """
    # Default values
    c_dst_class = data
    c_dst_method = None
    c_local_args = None
    c_dst_args = None
    c_ret = None

    # The call looks like this
    #  <destination class>) -> <method>(args)<return value>
    match = regex_method_call.search(data)

    if match:
        c_dst_class = match.group('dst_class')
        c_dst_method = match.group('dst_method')
        c_dst_args = match.group('dst_args')
        c_local_args = match.group('local_args')
        c_ret = match.group('return')

    c = {
        # Destination class
        'to_class': c_dst_class,

        # Destination method
        'to_method': c_dst_method,

        # Local arguments
        'local_args': c_local_args,

        # Destination arguments
        'dst_args': c_dst_args,

        # Return value
        'return': c_ret
    }

    return c


def extract_aput_object(data):
    """Extract aput-object from a string

    :data: Data would be sth like: v2, v0, v1

    :return: Returns an aput-object, otherwise None
    :rtype: dict
    """
    match = regex_extract_aput_object.search(data)

    if match:
        # An aput-object is usually saved in this form
        #  <referenced const string>, <array variable>, <index in the array>

        a = {
            # referenced const string
            'reference': match.group('reference'),

            # array var
            'array': match.group('array'),

            # reference index
            'index': match.group('index')
        }

        return a
    else:
        return None


def extract_iput_object(data):
    """Extract iput-object from a string

    :data: Data would be sth like: v0, p0, Lcom/example/package/class;->varname:[Ljava/lang/String;

    :return: Returns an iput-object, otherwise None
    :rtype: dict
    """
    match = regex_extract_iput_object.search(data)

    if match:
        # An aput-object is usually saved in this form
        #  <referenced variable>, <instance reference>, <package>;-><variable name>:<variable type>;

        i = {
            # referenced variable
            'reference': match.group('ref'),

            # instance reference
            'instance': match.group('instance'),

            # package
            'package': match.group('pkg'),

            # variable name
            'variable_name': match.group('name'),

            # type
            'type': match.group('type')
        }

        return i
    else:
        return None


def extract_sput_object(data):
    """Extract sput-object from a string

    :data: Data would be sth like: v0, Lcom/example/package/class;->varname:[Ljava/lang/String;

    :return: Returns a sput-object, otherwise None
    :rtype: dict
    """
    match = regex_extract_sput_object.search(data)

    if match:
        # An aput-object is usually saved in this form
        #  <referenced variable>, <package>;-><variable name>:<variable type>;

        s = {
            # referenced variable
            'reference': match.group('ref'),

            # package
            'package': match.group('pkg'),

            # variable name
            'variable_name': match.group('name'),

            # type
            'type': match.group('type')
        }

        return s
    else:
        return None


def extract_local_debug_info(data):
    """Extract .local debug information

    :data: Data would be sth like: .local v1, "future":Lcom/android/volley/toolbox/RequestFuture;,
    "Lcom/android/volley/toolbox/RequestFuture<Ljava/lang/Void;>;"

    :return: Returns a const string object, otherwise None
    :rtype: dict
    """
    match = regex_extract_local.search(data)

    if match:
        # A .local debug info is usually saved in this form
        #  <variable>,<variable name>:<type>;<type signature>

        l = {
            # Variable
            'name': match.group('var'),

            # Value of string
            'variable_name': match.group('name'),

            # Type of variable
            'type': match.group('type'),

            # Other part of the line
            'type_signature': match.group('signature')
        }

        return l
    else:
        return None


def main(argv):
    if len(argv) != 2:
        print("Usage: python {0} path/to/smali/file.smali".format(argv[0]))
        return
    logging.basicConfig(level=logging.DEBUG)
    test_instance = SmaliParser(argv[1])
    strings = test_instance.get_strings()
    strings.sort(key=lambda x: x.value)
    for s in strings:
        print("{0}".format(s))


if __name__ == '__main__':
    main(sys.argv)

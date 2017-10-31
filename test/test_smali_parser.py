import os
import unittest

from my_tools.smali_parser import SmaliParser

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class ContainsInstances(unittest.TestCase):
    """SmaliParser should be able to parse certain predetermined strings in a test smali file"""

    def test_get_strings(self):
        parser = SmaliParser(os.path.join(__location__, "JavaKey.smali"))
        mystrings = parser.get_strings()

        static_final_var = {'method_name': '', 'parameter_of': None,
                            'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                            'source': 'TYPE_STATIC_VAR', 'value': 'GIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4',
                            'in_array': False,
                            'name': 'API_KEY_FINAL_STATIC'}
        contains_static_final_var = False
        static_var = {'method_name': '<clinit>', 'parameter_of': None,
                      'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                      'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_STATIC_VAR',
                      'value': 'FIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': False, 'name': 'apiKeyStatic'}
        contains_static_var = False
        static_array1 = {'method_name': '<clinit>', 'parameter_of': None,
                         'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                         'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_STATIC_VAR',
                         'value': 'TIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                         'name': 'apiKeyStaticArray'}
        contains_static_array1 = False
        static_array2 = {'method_name': '<clinit>', 'parameter_of': None,
                         'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                         'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_STATIC_VAR',
                         'value': 'UIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                         'name': 'apiKeyStaticArray'}
        contains_static_array2 = False
        static_final_array1 = {'method_name': '<clinit>', 'parameter_of': None,
                               'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                               'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_STATIC_VAR',
                               'value': 'VIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                               'name': 'API_KEY_FINAL_STATIC_ARRAY'}
        contains_static_final_array1 = False
        static_final_array2 = {'method_name': '<clinit>', 'parameter_of': None,
                               'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                               'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_STATIC_VAR',
                               'value': 'WIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                               'name': 'API_KEY_FINAL_STATIC_ARRAY'}
        contains_static_final_array2 = False
        global_public_var = {'method_name': '<init>', 'parameter_of': None,
                             'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                             'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_INSTANCE_VAR',
                             'value': 'DIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': False,
                             'name': 'apiKeyPublic'}
        contains_global_public_var = False
        global_public_array1 = {'method_name': '<init>', 'parameter_of': None,
                                'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                                'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_INSTANCE_VAR',
                                'value': 'PIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                                'name': 'apiKeyPublicArray'}
        contains_global_public_array1 = False
        global_public_array2 = {'method_name': '<init>', 'parameter_of': None,
                                'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                                'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_INSTANCE_VAR',
                                'value': 'QIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                                'name': 'apiKeyPublicArray'}
        contains_global_public_array2 = False
        global_private_var = {'method_name': '<init>', 'parameter_of': None,
                              'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                              'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_INSTANCE_VAR',
                              'value': 'EIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': False,
                              'name': 'apiKeyPrivate'}
        contains_global_private_var = False
        global_private_array1 = {'method_name': '<init>', 'parameter_of': None,
                                 'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                                 'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_INSTANCE_VAR',
                                 'value': 'RIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                                 'name': 'apiKeyPrivateArray'}
        contains_global_private_array1 = False
        global_private_array2 = {'method_name': '<init>', 'parameter_of': None,
                                 'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                                 'source': 'TYPE_LOCAL_VAR', 'string_type': 'TYPE_INSTANCE_VAR',
                                 'value': 'SIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                                 'name': 'apiKeyPrivateArray'}
        contains_global_private_array2 = False
        local_var = {'method_name': 'getLocalKey', 'parameter_of': None,
                     'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                     'value': 'BIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': False, 'name': 'apiKeyLocal'}
        contains_local_var = False
        local_array1 = {'method_name': 'getLocalKeyArray', 'parameter_of': None,
                        'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                        'value': 'LIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                        'name': 'apiKeyLocalArray'}
        contains_local_array1 = False
        local_array2 = {'method_name': 'getLocalKeyArray', 'parameter_of': None,
                        'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                        'value': 'MIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                        'name': 'apiKeyLocalArray'}
        contains_local_array2 = False
        method_return = {'method_name': 'getLocalReturnKey', 'parameter_of': None,
                         'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                         'value': 'CIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': False, 'name': 'v0'}
        contains_method_return = False
        method_return_array1 = {'method_name': 'getLocalReturnKeyArray', 'parameter_of': None,
                                'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                                'value': 'NIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True, 'name': 'v2'}
        contains_method_return_array1 = False
        method_return_array2 = {'method_name': 'getLocalReturnKeyArray', 'parameter_of': None,
                                'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                                'value': 'OIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True, 'name': 'v2'}
        contains_method_return_array2 = False
        method_parameter = {'method_name': 'printKey', 'parameter_of': 'Ljava/util/Arrays.toString',
                            'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey', 'source': 'TYPE_LOCAL_VAR',
                            'string_type': 'TYPE_METHOD_PARAMETER', 'value': 'KIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4',
                            'in_array': False,
                            'name': 'v1'}
        contains_method_parameter = False
        method_parameter_array1 = {'method_name': 'printKeyArray', 'parameter_of': 'Ljava/util/Arrays.toString',
                                   'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                                   'source': 'TYPE_LOCAL_VAR',
                                   'string_type': 'TYPE_METHOD_PARAMETER',
                                   'value': 'XIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                                   'name': 'v3'}
        contains_method_parameter_array1 = False
        method_parameter_array2 = {'method_name': 'printKeyArray', 'parameter_of': 'Ljava/util/Arrays.toString',
                                   'class_name': 'Lit/uniroma2/adidiego/apikeytestapp/JavaKey',
                                   'source': 'TYPE_LOCAL_VAR',
                                   'string_type': 'TYPE_METHOD_PARAMETER',
                                   'value': 'YIzaSyCuxR_sUTfFJZBDkIsauakeuqXaFxhbur4', 'in_array': True,
                                   'name': 'v3'}
        contains_method_parameter_array2 = False

        for mystring in mystrings:
            if mystring.__dict__ == static_final_var:
                contains_static_final_var = True
            elif mystring.__dict__ == static_var:
                contains_static_var = True
            elif mystring.__dict__ == static_array1:
                contains_static_array1 = True
            elif mystring.__dict__ == static_array2:
                contains_static_array2 = True
            elif mystring.__dict__ == static_final_array1:
                contains_static_final_array1 = True
            elif mystring.__dict__ == static_final_array2:
                contains_static_final_array2 = True
            elif mystring.__dict__ == global_public_var:
                contains_global_public_var = True
            elif mystring.__dict__ == global_public_array1:
                contains_global_public_array1 = True
            elif mystring.__dict__ == global_public_array2:
                contains_global_public_array2 = True
            elif mystring.__dict__ == global_private_var:
                contains_global_private_var = True
            elif mystring.__dict__ == global_private_array1:
                contains_global_private_array1 = True
            elif mystring.__dict__ == global_private_array2:
                contains_global_private_array2 = True
            elif mystring.__dict__ == local_var:
                contains_local_var = True
            elif mystring.__dict__ == local_array1:
                contains_local_array1 = True
            elif mystring.__dict__ == local_array2:
                contains_local_array2 = True
            elif mystring.__dict__ == method_return:
                contains_method_return = True
            elif mystring.__dict__ == method_return_array1:
                contains_method_return_array1 = True
            elif mystring.__dict__ == method_return_array2:
                contains_method_return_array2 = True
            elif mystring.__dict__ == method_parameter:
                contains_method_parameter = True
            elif mystring.__dict__ == method_parameter_array1:
                contains_method_parameter_array1 = True
            elif mystring.__dict__ == method_parameter_array2:
                contains_method_parameter_array2 = True
        self.assertTrue(contains_static_final_var)
        self.assertTrue(contains_static_var)
        self.assertTrue(contains_static_array1)
        self.assertTrue(contains_static_array2)
        self.assertTrue(contains_static_final_array1)
        self.assertTrue(contains_static_final_array2)
        self.assertTrue(contains_global_public_var)
        self.assertTrue(contains_global_public_array1)
        self.assertTrue(contains_global_public_array2)
        self.assertTrue(contains_global_private_var)
        self.assertTrue(contains_global_private_array1)
        self.assertTrue(contains_global_private_array2)
        self.assertTrue(contains_local_var)
        self.assertTrue(contains_local_array1)
        self.assertTrue(contains_local_array2)
        self.assertTrue(contains_method_return)
        self.assertTrue(contains_method_return_array1)
        self.assertTrue(contains_method_return_array2)
        self.assertTrue(contains_method_parameter)
        self.assertTrue(contains_method_parameter_array1)
        self.assertTrue(contains_method_parameter_array2)

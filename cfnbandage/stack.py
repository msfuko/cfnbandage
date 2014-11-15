from . import ConfObject
from . import validator


class StackSetting(ConfObject):

    props = {
        'Version': (basestring, True),
        'Service': (validator.alphanumeric_string, True),
        'Name': (validator.alphanumeric_string, True),
        'Region': (basestring, True),
        'Parameters': (dict, False)
    }



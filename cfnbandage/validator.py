import re
from . import Reference


def alphanumeric_string(s):
    return re.sub(r'[\W_]+', '', s)


def boolean(s):
    if s in [True, 1, '1', 'true', 'True']:
        return "true"
    if s in [False, 0, '0', 'false', 'False']:
        return "false"
    raise ValueError(s)


def reference(s):
    if isinstance(s, dict) and s.get('Ref'):
        #return s['Ref']
        return Reference(s)
    elif isinstance(s, basestring):
        return s
    raise ValueError(s)


def reference_list(rlist):
    if isinstance(rlist, list):
        for idx, s in enumerate(rlist):
            rlist[idx] = reference(s)
        return rlist
    raise ValueError(rlist)
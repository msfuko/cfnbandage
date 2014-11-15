import types
import logging


class BaseObject(object):
    """
    Base Object of input
    """
    def __init__(self, **entries):
        self.properties = {}
        self.__dict__.update(entries)

    def _check_type(self, name, value, expected_type):

        # if it's a function
        if isinstance(expected_type, types.FunctionType):
            try:
                getattr(self, self.dictname)[name] = expected_type(value)
                #self.Properties[name] = expected_type(value)
            except ValueError:
                self._raise_value_error(name, value, expected_type)

        # if it's a list
        elif isinstance(expected_type, list):
            if not isinstance(value, list):
                self._raise_type_error(name, value, expected_type)
            for v in value:
                if not isinstance(v, tuple(expected_type)):
                    self._raise_type_error(name, v, expected_type)

        # anyone else
        elif isinstance(value, expected_type):
            pass

        else:
            self._raise_type_error(name, value, expected_type)

    #def __setattr__(self, name, value):
    def validate(self):
        if hasattr(self, self.dictname):
            properties = getattr(self, self.dictname)
            for name, (prop_type, required) in self.props.items():
                value = properties.get(name)
                self._check_type(name, value, prop_type)

                #if required and name not in self.Properties.keys():
                if required and name not in properties.keys():
                    errtype = getattr(self, 'type', "<unknown type>")
                    raise ValueError("resource %s required in type %s" % (name, errtype))

    @staticmethod
    def _raise_type_error(name, value, expected_type):
        raise TypeError('%s is %s, expected %s' % (name, type(value), expected_type))

    @staticmethod
    def _raise_value_error(name, value, expected_type):
        raise ValueError('\"%s\" value is illegal - %s with type %s' % (name, value, expected_type))


class AWSObject(BaseObject):

    dictname = 'Properties'
    logger = logging.getLogger(__name__)    #TODO: delete me
    _connection = None

    def patch(self, conn):
        raise NotImplementedError("this method is not implemented yet")

    def depends_on(self, cfn_conn, cfn_stack_id):
        raise NotImplementedError("Must implement depends on function")

    def set_connection(self, conn):
        self._connection = conn

    #FIXME
    def reference(self, parameters):
        """
        replace the reference of user input parameters
        """
        properties = getattr(self, self.dictname)
        for k, v in properties.items():
            if isinstance(v, Reference):
                if v.data in parameters.keys():
                    print "%s becomes %s" % (getattr(self, self.dictname)[k], parameters[v.data])
                    getattr(self, self.dictname)[k] = parameters[v.data]


class ConfObject(BaseObject):

    dictname = 'Stack'


# FIXME
class AWSHelperFn():
    """
    AWS Helper Function (e.g. Join, Reference, FindInMap, ...etc)
    """
    pass


class Reference(AWSHelperFn):

    def __init__(self, data):
        self.data = data['Ref']

    def __repr__(self):
        return self.data

    def get_data(self, parameters):
        return parameters.get(self.data, self)




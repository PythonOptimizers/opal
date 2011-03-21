import string

from opal.core.data import Data, DataSet

class Parameter(Data):
    """
    An abstract class to represent real, integer and categorical algorithmic
    parameters. Examples:

      >>> x = Parameter()        # A real parameter with no default value
      >>> n = Parameter(kind='integer', default=3)
      >>> choice = Parameter(kind='categorical', default='left')

    Parameters can be given a name:

      >>> delmin = Parameter(default=1.0e-3, name='DELMIN')

    Their value can be changed from their default value:

      >>> delmin.set_value(0.1)

    Their default value is still available:

      >>> print delmin.get_default()
      1.0e-3

    The bounds on a parameter may be a tuple indicating the lower and upper
    bounds if the parameter has an ordered kind, such as integer or real. 
    Otherwise, `bound` is a set of feasible values.
    """

    def __init__(self, kind='real', default=None, bound=None, name=None,
                 description='', **kwargs):
        if kind not in ['real', 'integer', 'binary', 'categorical']:
            raise TypeError, 'kind must be real, integer or categorical'

        if kind == 'real' and type(default) != type(0.0):
            raise ValueError, 'default value must agree with type'

        if kind == 'integer' and type(default) != type(0):
            raise ValueError, 'default value must agree with type'

        self.kind = kind

        self.is_real = (kind == 'real')
        self.is_integer = (kind == 'integer')
        self.is_categorical = (kind == 'categorical')

        # The attribute value store the value of parameter in run time.
        # this is a run-time information
        # The _default is a description
        if default is not None:
            if kind == 'real' and type(default) != type(0.0):
                raise ValueError, 'default value must agree with type'
            if kind == 'integer' and type(default) != type(0):
                raise ValueError, 'default value must agree with type'
            self._default = default
        else:
            if self.kind == 'real':
                self._default = 0.0
            elif self.kind == 'integer':
                self._default = 0
            elif self.kind == 'binary':
                self._default = True
            else:
                self._default = 'something'
        
        Data.__init__(self,
                      name=name,
                      description=description,
                      type=kind,
                      value=self._default,
                      dimension=1,
                      domain=bound)
        self.bound = bound
        return

    def get_default(self):
        "Return default value"
        return self._default
    
    def set_default(self,value):
        "Set default value."
        if self.is_real:
            self._default = float(value)
        elif self.is_integer:
            self._default = int(value)
        else:
            self._default = value
        self.value = self._default
        return

    def set_value(self, value):
        "Set parameter value to a non-default value."
        if value is None:
            self.value = self._default
            return
        if self.is_real:
            self.value = float(value)
        elif self.is_integer:
            self.value = int(value)
        else:
            self.value = value
        return

    def set_as_const(self):
        "Treat parameter as a constant."
        self.kind = 'const'
        return

    def get_kind(self):
        "Return parameter kind."
        return self.kind

    def is_const(self):
        "Return True if parameter is being treated as a constant."
        return self.kind == 'const'

    def set_bound(self, bound):
        """
        Set bounds on the parameter. For parameters of ordered kind,
        `set_bound((None, 0))` means that the lower bound is unchanged while
        the upper bound is reset to zero. For parameters of unordered kind,
        `set_bound` simply reassigns the list of feasible values.
        """
        if self.is_categorical:
            self.bound = bound
        else:
            if self.bound is None:
                self.bound = (None, None)
            if bound[0] is not None:
                self.bound[0] = bound[0]
            if bound[1] is not None:
                self.bound[1] = bound[1]
        return

    def get_bound(self):
        "Return bounds on the parameter."
        return self.bound
    
    def is_valid(self, value=None):
        """
        Checks whether or not the specified value falls within the allowed
        range for this parameter. If `value` is None, the current value of
        the parameter is used.
        """
       
        if value is not None:
            valueToVerify = value
        else:
            valueToVerify = self.value
        if self.bound is None:
            return True
        if self.is_categorical:
            return valueToVerify in self.bound
        # There is the error in transforming from string to int or float
        # For example, the value 0.0010000000 (in string in input file) is 
        # 0.00100000000001 after forcing it as real number
        # Pay attention to verify the bound at bounded point
        if self.bound[0] is not None:
            if valueToVerify < self.bound[0]:
                return False
        if self.bound[1] is not None:
            if valueToVerify > self.bound[1]:
                return False
        return True

    def export_to_dict(self):
        """
        Convert `Parameter` object to a dictionary.

        .. warning::

            This does not include the bounds!!!
        """
        return {'kind':self.kind,
                'name':self.name,
                'value':self.value,
                'default':self._default}


class ParameterSet(DataSet):
    """
    .. warning::

        Document this class!!!
    """

    def __init__(self, name='', storage='parameters.txt', parameters=[],
                 *args,**kwargs):

        DataSet.__init__(self,name=name,storage=storage,*args,**kwargs)

        # We store parameters in a list instead of a dictionary
        # to conserve the natural order defined by each algorithm
        # if use the dictionary, the order is the alphabet of the name
        self.parameters = parameters

        # The indices has elements in form (name:index) to accelerate
        # the searching by name
        self.indices = {}
        if len(self.parameters) > 0:
            for i in range(len(self.parameters)):
                self.indices[self.parameters[i].name] = i
        pass

    def __getitem__(self,id):
        if type(id) == type(0) :
            return self.parameters[id]
        index = self.indices[id]
        return self.parameters[index]

    def __len__(self):
        return len(self.parameters)

    def __contains__(self,parameterName):
        return (parameterName in self.indices.keys())

    def set_values(self, parameterValues=None, *args, **kwargs):
        # Verify if the parameter values are provided
        # if not, run the process with default values
        # Create the two value storages: a list and a dictionary
        # The list contains the values not specified name of parameters
        # They will be set by the order to the parameters list
        # The dictionary contains the values for the parameters whose names 
        # are specified in dictionary's keys.
        if parameterValues is None:
            # Set value to the default
            for param in self.parameters:
                param.set_value(None)

        valueList = []
        valueDict = {}
        if type(parameterValues) == type([]) or type(parameterValues) == type((1,)) :
            valueList.extend(parameterValues)
        elif type(parameterValues) == type({}):
            valueDict.update(parameterValues)
        else:
            valueList.append(parameterValues)
        valueList.extend(args)
        valueDict.update(kwargs)
        
        # Set the values in the list first
        for param, value in itertools.izip(self.parameters,valueList):
            param.set_value(value)
        # The values in the dictionary is added of
        # correct the ones are set by the list
        for paramName in valueDict.keys():
            if paramName in self.indices.keys():
                self.parameters[self.indices[paramName]].set_value(valueDict[paramName])
        return

    @staticmethod
    def check(valueList):
        return True

    @staticmethod
    def create_data(**options):
        return None


class ParameterConstraint:
    """
    .. warning::

        Document this class!!!
    """

    violated = False
    def __init__(self,constraintStr='',*argv):
        self.constraintStr = constraintStr
        pass

    def __call__(self,parameters):
        constraintStr = self.constraintStr
        for param in parameters :
            constraintStr = constraintStr.replace(param.name,str(param.value))
        return eval(constraintStr)


def _test():
    import doctest
    return doctest.testmod()
            

def test_parameter_class():
    p = Parameter(name='real_param')
    return

if __name__ == "__main__":
    _test()


import string

class Parameter:
    """
    An abstract class to represent real, integer and categorical algorithmic
    parameters. Examples:

      >>> x = AlgorithmicParameter()        # A real parameter with value 0
      >>> n = AlgorithmicParameter(kind='integer', default=3)
      >>> choice = AlgorithmicParameter(kind='categorical', default='left')

    Parameters can be given a name:

      >>> delmin = AlgorithmicParameter(default=1.0e-3, name='DELMIN')

    Their value can be changed from their default value:

      >>> delmin.set_value(0.1)

    Their default value is still available:

      >>> print delmin.get_default()
      1.0e-3
    """

    def __init__(self, kind='real', default=0.0, bounds=None,name=None, **kwargs):
        if kind not in ['real', 'integer', 'categorical']:
            raise TypeError, 'kind must be real, integer or categorical'

        if kind == 'real' and type(default) != type(0.0):
            raise ValueError, 'default value must agree with type'

        if kind == 'integer' and type(default) != type(0):
            raise ValueError, 'default value must agree with type'

        self.kind = kind

        self.is_real = (kind == 'real')
        self.is_integer = (kind == 'integer')
        self.is_categorical = (kind == 'categorical')

        self.name = name
        
        # The attribute value store the value of parameter in run time.
        # this is a run-time information
        # The _default is a description
        self._default = default
        self.value = default
        # The bounds of a parameter might be a tuple indicating 
        # the lower and the upper if the parameter has ordered kind 
        # like integer, real
        # Otherwise, bounds is a set of feasible values
        # In the default case, we have not any information about the 
        # bounds, we set it to None
        self.bounds = bounds
        return

    def get_default(self):
        "Return default value"
        return self._default

    def set_value(self, value):
        "Set parameter to a non-default value."
        if self.is_real:
            self.value = float(value)
        elif self.is_integer:
            self.value = int(value)
        else:
            self.value = value
        return

    def set_as_const(self):
        self.kind = 'const'
        return

    def get_kind(self):
        "Return parameter kind."
        return self.kind

    def is_const(self):
        return self.kind == 'const'

    def set_bounds(self,bounds):
        # This method to set the bounds for a parameter
        # For the ordered parameter:
        # set_bounds((None,0)) means we don't want to change
        # the lower bound that may be set before and change the
        # upper bound to 0.
        # For the non ordered one, this method is simply reassign
        # the list of feasible values
        if self.is_categorical :
            self.bounds = bounds
        else:
            if self.bounds is None:
                self.bounds = (None,None)
            if bounds[0] is not None:
                self.bounds[0] = bounds[0]
            if bounds[1] is not None:
                self.bounds[1] = bounds[1]
        return

    def get_bounds(self):
        # Get the bounds of variables
        return self.bounds
    
    def is_valid(self,value=None):
        # This method is to verify a value of parameter is valid or not
        # In the case, the value is not provided, the value of the parameter 
        # is verified
       
        if value is not None:
            valueToVerify = value
        else:
            valueToVerify = self.value
        if self.bounds is None:
            return True
        if self.is_categorical:
            return valueToVerify in self.bounds
        # There is the error in transforming from string to int or float
        # For example, the value 0.0010000000 (in string in input file) is 
        # 0.00100000000001 after forcing it as real number
        # Pay attention to verify the bounds at bounded point
        if self.bounds[0] is not None:
            if valueToVerify < self.bounds[0]:
                #print 'Less than lower bound', valueToVerify - self.bounds[0]
                return False
        if self.bounds[1] is not None:
            if valueToVerify > self.bounds[1]:
                #print 'Greater than upper bound', valueToVerify - self.bounds[1]
                return False
        return True

    def export_to_dict(self):
        return {'kind':self.kind,
                'name':self.name,
                'value':self.value,
                'default':self._default}


class ParameterConstraint:
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
            
if __name__ == "__main__":
    _test()


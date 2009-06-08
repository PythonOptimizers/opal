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

    def __init__(self, kind='real', default=0.0, name=None, **kwargs):
        if kind not in ['real', 'integer', 'categorical']:
            raise TypeError, 'kind must be real, integer or categorical'

        if kind == 'real' and type(default) != type(0.0):
            raise ValueError, 'default value must agree with type'

        if kind == 'integer' and type(default) != type(0):
            raise ValueError, 'default value must agree with type'

        self.kind = kind
        self.name = name

        self.is_real = (kind == 'real')
        self.is_integer = (kind == 'integer')
        self.is_categorical = (kind == 'categorical')

        self._default = default
        self.value = default
        return

    def get_default(self):
        "Return default value"
        return self._default

    def set_value(self, value):
        "Set parameter to a non-default value."
        if self.is_real:
            self.value = float(value)
        if self.is_integer:
            self.value = int(value)
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


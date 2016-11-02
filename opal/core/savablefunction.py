import sys
import os.path
import marshal
import new
import log

class SavableFunction:
    """
    This class contains the information of a measure function that
    built up from the parameter and elementary measure \varphi(p,\mu)
    """
    def __init__(self, function=None, name=None,**kwargs):
        if function is None:
            raise Exception('The savable function definition is invalid')
        # The information of a function include all possible description
        # such as convexity, ... Any information is accepted
        # We concentrate on a property called possitively-additive.
        # A function objective is called possitively-additive if function value
        # of partial data is always less than or equal to the data-full one

        self.information = {}
        self.information.update(kwargs)
        # It's important to define a function with two arguments:
        #the parameter and the measure
        # We check if the given function sastifies this constraint:

        self.func = function
        if name is None:
            self.name = function.__code__.co_name
        else:
            self.name = name
        #self.name = function.__code__.co_name
        #self.code_string = None
        pass

    def evaluate(self, *args, **kwargs):
        if self.func is  None:
            raise Exception('The measure function is not defined')
        return self.func(*args, **kwargs)
        #self.load()
        #value = self.func(*args, **kwargs)
        #del self.func
        #self.func = None # Keep self.func is None for the next pickling
        #return value

    def __getstate__(self):
        content = {}
        content['code'] = marshal.dumps(self.func.__code__)
        content['information'] = self.information
        content['name'] = self.name
        return content

    def __setstate__(self, content):
        self.func = new.function(marshal.loads(content['code']),globals())
        self.information = content['information']
        self.name = content['name']
        return

    def __call__(self,*args,**kwargs):
        return self.evaluate(*args,**kwargs)



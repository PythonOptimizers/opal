import sys
import os.path
import marshal
import new
import log

class MeasureFunction:
    """
    *** This class contains the information of a measure function that
    *** built up from the parameter and elementary measure \varphi(p,\mu)
    """
    def __init__(self,function=None):
        if function is None:
            return
        '''
        It's important to define a function with two arguments: 
        the parameter and the measure
        We check if the given function sastifies this constraint:
        '''
        if function.__code__.co_argcount < 2:
            return
        self.func = function
        self.name = function.__code__.co_name    
        #self.name = function.__code__.co_name
        pass

    def evaluate(self, *args, **kwargs):
        if self.func is not  None:
            return self.func(*args, **kwargs)
        self.load()
        value = self.func(*args, **kwargs)
        del self.func
        self.func = None # Keep self.func is None for the next pickling
        return value
               
    def save(self, dir='./', fileName=None):
        if fileName is None:
            self.file_name = os.path.abspath(dir) + '/' + self.func.__code__.co_name + '.code'
        else: 
            self.file_name = os.path.abspath(dir) + '/' + fileName 
        if self.func is None:
            return
        f = open(self.file_name,'w')
        marshal.dump(self.func.__code__,f)
        f.close()
        self.func = None # This is neccessary for pickling a measure function. 
        return

    def load(self, fileName=None):
        f = open(self.file_name)
        self.func = new.function(marshal.load(f),globals()) 
        f.close()
        return
    
    def __getstate__(self):
        content = {}
        content['code'] = marshal.dumps(self.func.__code__)
        return content

    def __setstate__(self, content):
        self.func = new.function(marshal.loads(content['code']),globals()) 
        return
        
    def __call__(self,*args,**kwargs):
        return self.evaluate(*args,**kwargs)

class Constraint:
    """
    *** This class is a description constraint. A constraint is defined in form
    *** lower_bound <= measure_function <= upper_bound
    *** if lower_bound is None, the constraint is consider as 
    *** measure_function <= upper_bound
    *** The same principle is applied to upper_bound
    *** To define a constraint, there is at least a bound is not Non
    """
    def __init__(self, function=None,lowerBound=None,upperBound=None,**kwargs):
        self.function = MeasureFunction(function)
        self.lower_bound = lowerBound
        self.upper_bound = upperBound
        return
    
    def evaluate(self,*args,**kwargs):
        funcVal = self.function(*args,**kwargs)
        values = [None,None]
        if self.lower_bound is not None:
            values[0] = self.lower_bound - funcVal
        if self.upper_bound is not None:
            values[1] = funcVal - self.upper_bound
        return values


class ModelStructure:
    """
    
    An object of this class represent for the model structure that is 
    described in Python language. The evaluator accept only ModelStructure 
    object as structure of model. Any structure modeled by other language 
    such as AMPL has to be rewritten as a ModelStructure object. This 
    can be done by the interpreters.
    """
    def __init__(self,
                 name='modelstruct',
                 objective=None, 
                 constraints=[]):
        self.name = name
        self.objective = MeasureFunction(objective)
        self.constraints = []
        if constraints is not None:
            for cons in constraints:
                constraint = Constraint(lowerBound=cons[0], 
                                        function=cons[1],
                                        upperBound=cons[2])
                self.constraints.append(constraint)
        return
        
    def save(self):
        
        return

    def load(self, file=None):
        return
   

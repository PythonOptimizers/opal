import sys
import os.path
import marshal
import new
import log

class MeasureFunction:
    """
    This class contains the information of a measure function that
    built up from the parameter and elementary measure \varphi(p,\mu)
    """
    def __init__(self, function=None, **kwargs):
        if function is None:
            raise Exception('Measure function definition is invalid')
        # The information of a function include all possible description
        # such as convexity, ... Any information is accepted
        # We concentrate on a property called possitively-additive.
        # A function objective is called possitively-additive if function value
        # of partial data is always less than or equal to the data-full one
        
        self.information = {'additivity':0, # Undetermined
                                            # additivity = 1 means
                                            # function is possitively-
                                            # additivity. And = -1 if this
                                            # is a negatively-additive

                            'convexity':0 # Undetermined
                            }
        self.information.update(kwargs)
        # It's important to define a function with two arguments: 
        #the parameter and the measure
        # We check if the given function sastifies this constraint:

        if function.__code__.co_argcount < 2:
            return
        self.func = function
        self.name = function.__code__.co_name    
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
               
    ## def save(self, dir='./', fileName=None):
        
    ##     if self.func is None:
    ##         return
    ##     if fileName is None: # Dump to string
    ##         self.file_name = None
    ##         self.code_string = marshal.dumps(self.func.__code___)
    ##     else: 
    ##         self.file_name = os.path.abspath(dir) + '/' + fileName 
    ##         f = open(self.file_name,'w')
    ##         marshal.dump(self.func.__code__,f)
    ##         f.close()
    ##     self.func = None # This is neccessary for pickling a measure function. 
    ##     return

    ## def load(self, fileName=None):
    ##     if self.file_name is not None:
    ##         f = open(self.file_name)
    ##         self.func = new.function(marshal.load(f),globals()) 
    ##         f.close()
    ##     else: # Load from code string
    ##         self.func = new.function(marshal.loads(self.code_string),
    ##                                  globals())
    ##     return
    
    def __getstate__(self):
        content = {}
        content['code'] = marshal.dumps(self.func.__code__)
        content['information'] = self.information
        return content

    def __setstate__(self, content):
        self.func = new.function(marshal.loads(content['code']),globals())
        self.information = content['information']
        return
        
    def __call__(self,*args,**kwargs):
        return self.evaluate(*args,**kwargs)

    # Because measure function is kind of special for our
    # problem. Some properties is exploited here, for example
    # positively-additvie
    def add_information(self, **kwargs):
        self.information.update(kwargs)
        
    def is_positively_additive(self):
        return self.information['additivity'] > 0

    def is_negatively_additive(self):
        return self.information['additivity'] < 0

class Objective:
    """

    A funciton objective with internal dynamically updated bound
    """
    def __init__(self,
                 function=None,
                 name='objective',
                 lowerBound=None,
                 upperBound=None,
                 **kwargs):
        self.name = name
        if isinstance(function, MeasureFunction):
            self.function = function
            self.function.add_information(**kwargs)
        else:
            self.function = MeasureFunction(function, **kwargs)
        self.lower_bound = lowerBound
        self.upper_bound = upperBound
        return
    
    def evaluate(self, *args, **kwargs):
        funcVal = self.function(*args, **kwargs)
        return funcVal

    def update_bounds(self, funcVal):
        log.debugger.log('Bounds ' + \
                         str((self.lower_bound, self.upper_bound)) + \
                         ' on bbjective function is updated by new value ' + \
                         str(funcVal))
        if self.lower_bound is None:
            self.lower_bound = funcVal
        elif funcVal < self.lower_bound:
            self.lower_bound = funcVal

        if self.upper_bound is None:
            self.upper_bound = funcVal
        elif funcVal > self.upper_bound:
            self.upper_bound = funcVal
        return

    def is_partially_exceed(self, val):
        # Suppose that we work always with a minimization problem
        if not self.function.is_positively_additive():
            # If the function is not positively-additive, we could not
            # determine if it is partially exceed
            return False
        if self.lower_bound is not None: # A bound exists
            return (val > self.lower_bound)
        return False 
      

        
class Constraint:
    """

    This class is a description constraint. A constraint is defined in form
       lower_bound <= measure_function <= upper_boun
    if lower_bound is None, the constraint is consider as 
       measure_function <= upper_bound  
    The same principle is applied to upper_bound

    To define a constraint, there is at least a bound is not None. 
    """

    def __init__(self,
                 function=None,
                 lowerBound=None,
                 upperBound=None,
                 name='constraint',
                 **kwargs):
        if (lowerBound is None) and (upperBound is None):
            raise Exception('Constraint definition is invalid')
        self.name = name
        if isinstance(function, MeasureFunction):
            self.function = function
            self.function.add_information(**kwargs)
        else:
            self.function = MeasureFunction(function, **kwargs)      
        self.n_size = 2
        self.lower_bound = lowerBound
        if self.lower_bound is None:
            self.n_size = self.n_size - 1
        self.upper_bound = upperBound
        if self.upper_bound is None:
            self.n_size = self.n_size - 1
        return
    
    def evaluate(self, *args, **kwargs):
        funcVal = self.function(*args,**kwargs)
        values = []
        if self.lower_bound is not None:
            values.append(self.lower_bound - funcVal)
        else:
            values.append(None)

        if self.upper_bound is not None:
            values.append(funcVal - self.upper_bound)
        else:
            values.append(None)
        return values

    def is_partially_violated(self, val):
        # The partially-violated checking is feasible if the constraint
        # function is either positively-additive or negatively-additive
        if self.function.is_positively_additive():
            if self.upper_bound is not None:
                # log.debugger.log('The constraint is partially violated')
                return (val[1] > self.upper_bound)
            return False
        if self.function.is_negatively_additive():
            if self.lower_bound is not None:
                return (val[0] < self.lower_bound)
            return False
        # In the case of funtion's additive-behavior is undetermined,
        # the checking is not feasible
        return False

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
        if isinstance(objective, Objective):
            self.objective = objective
        else:
            self.objective = Objective(objective)
        self.constraints = []
        if constraints is not None:
            for cons in constraints:
                if isinstance(cons, Constraint):
                    self.constraints.append(cons)
                else:
                    constraint = Constraint(lowerBound=cons[0], 
                                            function=cons[1],
                                            upperBound=cons[2])
                    self.constraints.append(constraint)
        return
        

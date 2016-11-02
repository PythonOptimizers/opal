import sys
import os.path
import marshal
import new
import types 
import log


from savablefunction import SavableFunction

class MeasureFunction(SavableFunction):
    """
    This class contains the information of a measure function that
    built up from the parameter and elementary measure \varphi(p,\mu)
    """
    def __init__(self, function=None, **kwargs):
       
        SavableFunction.__init__(self, function, **kwargs)
        if function.__code__.co_argcount < 2:
            raise Exception("A measure function has at least two arguments")
        self.information = {'additivity':0, # Undetermined
                                            # additivity = 1 means
                                            # function is possitively-
                                            # additivity. And = -1 if this
                                            # is a negatively-additive

                            'convexity':0 # Undetermined
                            }
        self.information.update(kwargs)
       
        pass

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

    A function objective with internal dynamically updated bound
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
        #log.debugger.log('Bounds ' + \
        #                 str((self.lower_bound, self.upper_bound)) + \
        #                 ' on bbjective function is updated by new value ' + \
        #                 str(funcVal))
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
                 constraints=[],
                 **kwargs):
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
        # informations can contain any information about the structure,
        # this is the supplementary information in addition to two basic
        # information of the objective function and constraint
        # An example of this kind of information is the neighborhodd definition
        # that is user knowledge about the parameter space
        self.informations = {}
        self.informations.update(kwargs)
        # For information that is provided as an user-defined function,
        # it should be transformed to an SavableFunction object. This allows
        # to save the structure as a data file
        for infoName, info in self.informations.items():
            if isinstance(info, (types.FunctionType, types.BuiltinFunctionType)):
                self.informations[infoName] = SavableFunction(function=info,
                                                              name=infoName)
        return
        

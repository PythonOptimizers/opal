import sys
import os.path
import marshal
import new

class ModelStructure:
    """
    *** THIS IS LACKING DOCUMENTATION ***
    """
    def __init__(self, objective=None, constraints=[], **kwargs):
        self.objective = MeasureFunction(objective)
        self.constraints = constraints
        #for constraint in constraints:
        #    if type(constraint) == type((1,2)):
        #        self.constraints.append()
        #    else:
        #        self.constraints.append((MeasureFunction(constraint),0))
        self.log = None
        pass

class MeasureFunction:
    """
    *** This class contains the information of a measure function that
    *** built up from the parameter and elementary measure \varphi(p,\mu)
    """
    def __init__(self,function=None):
        if function is None:
            return
        # It's important to define a function with two arguments: the parameter and the measure
        # We check if the given function sastifies this constraint:
        if function.__code__.co_argcount < 2:
            return
        self.file_name = os.path.dirname(os.path.abspath(function.__code__.co_filename)) + '/' + function.__code__.co_name + '.code'
        f = open(self.file_name,'w')
        marshal.dump(function.__code__,f)
        f.close()
        self.name = function.__code__.co_name
        pass

    def evaluate(self,*args,**kwargs):

        f = open(self.file_name)
        function = new.function(marshal.load(f),globals())
        return function(*args,**kwargs)

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
        pass
    
    def evaluate(self,*args,**kwargs):
        funcVal = self.function(*args,**kwargs)
        values = [None,None]
        if self.lower_bound is not None:
            values[0] = self.lower_bound - funcVal
        if self.upper_bound is not None:
            values[1] = funcVal - self.upper_bound
        return values

class ModelEvaluator:
    def __init__(self,model=None,measures=None,logging=None,**kwargs):
        self.model = model
        self.measures = measures
        self.logging = logging
        pass

    def evaluate(self,testResult):
        if testResult.test_is_failed:
            consValues = []
            for i in range(len(self.model.constraints)):
                consValues.append(1.0e20)
            return (1.0e20,consValues)
        
        # Set the data for the used measures
        # This setting helps to take the value of the elementary measure
        for measure in self.measures:
            measure.set_data(testResult.measure_value_table)
        
        # Get the value of parameter vector p
        # paramValues = [param.value for param in testResult.parameters if not param.is_const()]
        # Get the optimizing parameter
        parameterSet = {}
        for param in testResult.parameters:
            if not param.is_const():
                parameterSet[param.name] = param
        measureValues = testResult.measure_value_table
        # Evaluate the objective function by passing the parameter vector and measure vector
        # The 
        objValue = self.model.objective(parameterSet,measureValues)
        consValues = []
        for i in range(len(self.model.constraints)):
            #consValues.append(self.model.constraints[i][0](paramValues,self.measures) - self.model.constraints[i][1]) 
            #consValues.append(self.model.constraints[i][0](parameterSet,measureValues) - self.model.constraints[i][1])
            consValues.extend([val for val in self.model.constraints[i].evaluate(parameterSet,measureValues) if val is not None])
        return (objValue,consValues)

    def log(self,fileName):
        if self.logging is not None:
            self.logging.write(fileName,self.result_string)
        return

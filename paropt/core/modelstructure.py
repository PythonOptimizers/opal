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
        self.constraints = []
        for constraint in constraints:
            if type(constraint) == type((1,2)):
                self.constraints.append((MeasureFunction(constraint[0]),
                                        constraint[1]))
            else:
                self.constraints.append((MeasureFunction(constraint),0))
        self.log = None
        pass

class MeasureFunction:
    """
    *** This class contains the information to evaluate it
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

class ModelEvaluator:


    def __init__(self,model=None,measures=None,**kwargs):
        self.model = model
        self.measures = measures
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
        paramValues = [param.value for param in testResult.parameters if not param.is_const()]
        measureValues = testResult.measure_value_table
        # Evaluate the objective function by passing the parameter vector and measure vector
        # The 
        objValue = self.model.objective(paramValues,measureValues)
        consValues = []
        for i in range(len(self.model.constraints)):
            #consValues.append(self.model.constraints[i][0](paramValues,self.measures) - self.model.constraints[i][1]) 
            consValues.append(self.model.constraints[i][0](paramValues,measureValues) - self.model.constraints[i][1])
        return (objValue,consValues)

    def log(self,fileName):
        return

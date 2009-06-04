import sys
import os.path
import marshal
import new

from ..Measures import *
class ModelStructure:
    """
    *** THIS IS LACKING DOCUMENTATION ***
    """
    def __init__(self, objective=None, constraints=None, **kwargs):
        self.objective = MeasureFunction(objective)
        self.constraints = []
        for constraint in constraints:
            if type(constraint) != type((1,2)):
                self.constraints.append(MeasureFunction(constraint[0]),constraint[1])
            else:
                self.constraints.append(MeasureFunction(constraint),0)
        self.log = None
        pass

class MeasureFunction:
    """
    *** This class contains the information to evaluate it
    """
    def __init__(self,function=None):
        if function is None:
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

class ObjectiveFunction:
    def __init__(self,measureTable=None,**kwargs):
        self. measureTable = measureTable
        pass
    
    def __call__(self,paramValues,**kwargs):
        return 0

class Constraint:
    def __init__(self,meauresTable,left,right,**kwargs):
        self.measureTable = measureTable
        self.left = left
        self.right = right
        pass
    
    def __call__(self,paramValues,**kwargs):
        return self.left(paramValues) - self.right(paramValues)

class ModelEvaluator:


    def __init__(self,model=None,related_measures=None,**kwargs):
        self.model = model
        self.related_measures = related_measures
        pass

    def evaluate(self,testResult):
        if testResult.test_is_failed:
            consValues = []
            for i in range(len(self.model.constraints)):
                consValues.append(1.0e20)
            return (1.0e20,consValues)
        
        for measure in self.related_measures:
            measure.get_global_object().set_data(testResult.measure_value_table)

        paramValues = [param.value for param in testResult.parameters if not param.is_const()]
        objValue = self.model.objective(paramValues)
        consValues = []
        for i in range(len(self.model.constraints)):
            consValues.append(self.model.constraints[i][0](paramValues) - self.model.constraints[i][1]) 
        return (objValue,consValues)

    def log(self,fileName):
        return

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
            
        f = open(self.file_name)
        func = new.function(marshal.load(f),globals()) # Keep self.func is None for the next pickling
        f.close()
        return func(*args, **kwargs)
               
    def dump(self, dir='./', fileName=None):
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
                 constraints=[], 
                 logHandlers=[],
                 **kwargs):
        self.name = name
        self.working_directory = './' + name
        if not os.path.exists(self.working_directory):
            os.mkdir(self.working_directory)
        self.objective = MeasureFunction(objective)
        self.objective.dump(dir=self.working_directory)
        #self.constraints = constraints
        self.constraints = []
        if constraints is not None:
            for cons in constraints:
                constraint = Constraint(lowerBound=cons[0], 
                                        function=cons[1],
                                        upperBound=cons[2])
                self.constraint.append(constraint)
                constraint.function.dump(dir=self.working_directory)
                
        self.logger = log.OPALLogger(name='modelStructure',
                                     handlers=logHandlers)
        return
        
    def evaluate(self,testResult):
        self.logger.log('Begin of a model evaluation')
        if testResult.test_is_failed:
            consValues = []
            for i in range(len(self.constraints)):
                consValues.append(1.0e20)
            self.logger.log(' - The model values are infinite')
            self.logger.log('End of a model evaluation')
            return (1.0e20,consValues)
        
        # Set the data for the used measures
        # This setting helps to take the value of the elementary measure
        #for measure in self.measures:
        #    measure.set_data(testResult.measure_value_table)
        
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
        objValue = self.objective(parameterSet,measureValues)
        consValues = []
        for i in range(len(self.constraints)):
            consValues.extend([val for val \
                                   in self.constraints[i].evaluate(parameterSet,
                                                                   measureValues) \
                                   if val is not None])
        self.logger.log(' - OBJ: ' + str(objValue) + \
                         ', CONS: ' + str(consValues))
        self.logger.log('End of model evaluation')
        return (objValue,consValues)


class ModelEvaluator(threading.Thread):
    def __init__(self,model=None,measures=None,logging=None,**kwargs):
        self.model = model
        self.logger = log.OPALLogger(name='modelStructure',
                                      handlers=logHandlers)
        pass

   
    def log(self,fileName):
        if self.logging is not None:
            self.logging.write(fileName,self.result_string)
        return

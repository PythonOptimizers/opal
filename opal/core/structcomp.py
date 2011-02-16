import sys
import os.path
import marshal
import new
import log


class StructureComputer(Broker):
    """
    
    An object of this class represent for the model structure that is 
    described in Python language. The evaluator accept only ModelStructure 
    object as structure of model. Any structure modeled by other language 
    such as AMPL has to be rewritten as a ModelStructure object. This 
    can be done by the interpreters.
    """
    def __init__(self,
                 name='structcomp',
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

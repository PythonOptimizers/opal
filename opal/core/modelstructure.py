import os.path
import marshal
import new
import log

__docformat__ = 'restructuredtext'

class ModelStructure:
    """
    *** THIS IS LACKING DOCUMENTATION ***
    """

    def __init__(self, name='modelstruct', objective=None, constraints=[],
                 logHandlers=[], **kwargs):

        self.name = name
        self.working_directory = './' + name
        if not os.path.exists(self.working_directory):
            os.mkdir(self.working_directory)
        self.objective = MeasureFunction(objective)
        self.objective.dump(dir=self.working_directory)
        self.constraints = []
        if constraints is not None:
            for cons in constraints:
                constraint = Constraint(lowerBound=cons[0],
                                        function=cons[1],
                                        upperBound=cons[2])
                self.constraints.append(constraint)
                constraint.function.dump(dir=self.working_directory)

        self.logger = log.OPALLogger(name='ModelStructure',
                                     handlers=logHandlers)
        self.logger.log('Initializing ModelStructure object')
        return


    def evaluate(self, testResult):

        self.logger.log('Start of a model evaluation')
        if testResult.test_is_failed:
            consValues = []
            for i in range(len(self.constraints)):
                consValues.append(1.0e20)
            self.logger.log('   Model values are infinite due to failure')
            self.logger.log('End of model evaluation')
            return (1.0e20, consValues)

        # Get the optimizing parameter
        parameterSet = {}
        for param in testResult.parameters:
            if not param.is_const():
                parameterSet[param.name] = param
        measureValues = testResult.measure_value_table

        # Evaluate the objective function by passing the parameter vector and
        # measure vector
        objValue = self.objective(parameterSet, measureValues)
        consValues = []
        for i in range(len(self.constraints)):
            consValues.extend([val for val \
                               in self.constraints[i].evaluate(parameterSet,
                                                               measureValues) \
                               if val is not None])
        self.logger.log('   OBJ: ' + str(objValue) + \
                         ', CONS: ' + str(consValues))
        self.logger.log('End of model evaluation')
        return (objValue,consValues)


class MeasureFunction:
    """
    *** This class contains the information of a measure function that
    *** built up from the parameter and elementary measure \varphi(p,\mu)
    """

    def __init__(self, function=None, logHandlers=[]):

        if function is None: return

        # It's important to define a function with two arguments:
        # the parameter and the measure
        # We check if the given function sastifies this constraint:
        if function.__code__.co_argcount < 2: return
        self.func = function
        self.name = function.__code__.co_name
        self.fileName = None
        self.logger = log.OPALLogger(name='MeasureFunction',
                                     handlers=logHandlers)
        self.logger.log('Initializing measure funtion %s' % self.name)
        return


    def evaluate(self, *args, **kwargs):

        self.logger.log('Evaluating measure function %s' % self.name)
        if self.func is not  None:
            return self.func(*args, **kwargs)

        f = open(self.file_name)
        func = new.function(marshal.load(f),globals())
        # Keep self.func is None for the next pickling
        f.close()
        return func(*args, **kwargs)


    def dump(self, dir='./', fileName=None):

        self.logger.log('Dumping measure function %s to disk' % self.name)
        if fileName is None:
            self.file_name = os.path.join(os.path.abspath(dir),
                                          self.func.__code__.co_name + '.code')
        else:
            self.file_name = os.path.join(os.path.abspath(dir), fileName)

        if self.func is None: return
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

    __classid = -1

    def __init__(self, function=None, lowerBound=None, upperBound=None,
                 name=None, logHandlers=[], **kwargs):

        # If name is not given, assign a unique constraint name.
        self.__class__.__classid += 1          # Number of instances.
        self.__id = self.__class__.__classid   # Instance number.

        if name is None:
            name = 'cons%d' % self.__id
        self.name = name

        self.function = MeasureFunction(function)
        self.n_size = 2
        self.lower_bound = lowerBound
        if self.lower_bound is None:
            self.n_size = self.n_size - 1
        self.upper_bound = upperBound
        if self.upper_bound is None:
            self.n_size = self.n_size - 1
        self.logger = log.OPALLogger(name='Constraint',
                                     handlers=logHandlers)
        self.logger.log('Initializing constraint %s' % self.name)
        return


    def evaluate(self,*args,**kwargs):

        self.logger.log('Evaluating constraint %s' % self.name)
        funcVal = self.function(*args,**kwargs)
        values = []
        if self.lower_bound is not None:
            values.append(self.lower_bound - funcVal)
        if self.upper_bound is not None:
            values.append(funcVal - self.upper_bound)
        return values


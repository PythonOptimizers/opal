import os
import string
import types
import time
import shutil
import log
import copy
#import logging

#import utility
from measure import MeasureValueTable
from testproblem import TestProblem

from .. import config


class TestResult:


    def __init__(self,
                 testIsFailed=None,
                 testNumber=None,
                 problems=None,
                 parameters=None,
                 measureValueTable=None,
                 **kwargs):
        self.test_is_failed = testIsFailed
        self.test_number = testNumber
        self.problems = problems
        self.parameters = parameters
        self.measure_value_table = measureValueTable
        pass
    


# =============================
class ModelData:
    """ 
    This class represents a data generator for a parameter optimization
    problem. The data is the values of the elementary measures that are needed
    to formulate the problem. To specify a data generator, we need provide:

    1. The algorithm 
    2. the set of elementary measures concerned 
    3. the set of parameters to control
    4. the test problems set.
    """

    def __init__(self, algorithm, problems, activeParameters,
                platform=config.platform, logHandlers=[], **kwargs):
        # The core variables
        self.algorithm = algorithm
        if (problems is None) or (len(problems) == 0):
            self.problems = [TestProblem(name='TESTPROB')]
        else:
            self.problems = problems
        
        self.parameters = activeParameters

        # active_parameters_names are the name of parameters that are
        # variables in the parameter optimization problem.
        # The other parameters remain fixed.
        #activeParamNames = [par.name for par in activeParameters]
        #for param in self.algorithm.parameters:
        #    if param.name not in activeParamNames:
        #        param.set_as_const()
        
        #self.parameters = copy.deepcopy(algorithm.parameters)
        self.measures = copy.deepcopy(algorithm.measures)
        
        # TODO
        # This is unrelated to the model data. It should be moved elsewhere.
        #self.platformName = ''
        self.platform = platform

        # By default, logger is Logger object of Python's logging module
        # Logger is set name to modeldata, level is info.
        self.logger = log.OPALLogger(name='modelData', handlers=logHandlers)
        # The monitor variables
        self.test_number = 0
        self.test_id = None

        # The output
        self.test_is_failed = False
        pNames = [prob.name for prob in self.problems]
        mNames = [measure.name for measure in self.measures]
        self.measure_value_table = MeasureValueTable(problem_names=pNames,
                                                     measure_names=mNames)
        # Set options

        #self.set_options(**kwargs)
        return


    #def set_options(self,**kwargs):
    #    # set the log file
    #    if 'logFile' in kwargs.keys():
    #        self.logFileName  = os.path.join(os.getcwd(), logFile)
    #    else:
    #        self.logFileName  = os.path.join(os.getcwd(), 'test-bed.log')
    #    return


    def get_parameters(self):
        return self.parameters


    #def fill_parameter_value(self,values):
    #    j = 0
    #    for i in range(len(self.parameters)):
    #        if not self.parameters[i].is_const():
    #            self.parameters[i].set_value(values[j])
    #            j = j + 1
    #    return

    def initialize(self, parameterValues):
        '''
        
        This method return an unique identity for the 
        test basing on the parameter values
    
        The identity obtains by hashing the parameter values string. 
        This is an inversable function. It means that we can get 
        the parameter_values form the id
        '''
        
        valuesStr = '_'
        j = 0
        for i in range(len(self.parameters)):
            self.parameters[i].set_value(parameterValues[j])
            valuesStr = valuesStr + str(parameterValues[j]) + '_'
            j = j + 1    
        self.test_id = str(hash(valuesStr))
        self.test_number += 1
        self.test_is_failed = False
        self.measure_value_table.clear()
        self.logger.log('Initialize the ' + str(self.test_number) + \
                         ' test with id ' + str(self.test_id))
        self.logger.log(' - Parameter values: ' + valuesStr.replace('_', ' ')) 
        return 

    def finalize(self):
        self.algorithm.clean_running_data(testId=self.test_id)
        self.logger.log('Finalize the test ' + str(self.test_id))
        return
        
    def run(self, parameterValues):
        self.initialize(parameterValues=parameterValues)
        #print '[modeldata.py]',[param.value for param in self.parameters]
        self.logger.log('Run the test ' + str(self.test_id))
        self.algorithm.set_parameter(parameters=self.parameters, 
                                     testId=self.test_id)
        if not self.algorithm.are_parameters_valid():
            #print '[modeldata.py]','Parameter values are invalid, test fails'
            self.test_is_failed = True
            self.logger.log(' - The parameter values are invalid, ' + \
                             'the test is stopped')
            return
        #print '[modeldata.py]','Parameter values are valid'
        
        #ltime = time.localtime()
        #self.run_id = str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
        #         str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        # Launches the algorithm routines
        
        #self.run_id = get_test_id(self, parameterValues)
        
        self.platform.initialize(self.test_id)
        self.logger.log(' - Solve the test problems') 
        for prob in self.problems:
            #print '[modeldata.py]:Executing ' + prob
            #if self.algorithm.get_output() is None:
                # The algorithm out the measues to standard output
                # We will redirect the output to the corresponding measure file
                # Otherwise, the output of runing is outed to the /dev/null
            #    output_file_name = algorithm.get_measure_file(prob)
            #else:
            #    output_file_name = '/dev/null'
            #output_file_name = self.algorithm.name + '-' + prob.name + '.out'
            self.platform.execute(\
                self.algorithm.get_full_executable_command(problem=prob, 
                                                           testId=self.test_id))
            
        resultIsReady = "numended(/g" + self.test_id + ", *)"
        self.platform.waitForCondition(resultIsReady)
        self.logger.log(' - All problems are solved, the test is stopped')
        return 

    def get_test_result(self):
        self.logger.log('Collect the test result')
        if self.test_is_failed is True:
            self.finalize()
            return TestResult(testIsFailed=True)
       
        for prob in self.problems:
            # We accept only a perfect measure values table, this means the 
            # atomic measure are get from all of the problems. Any error 
            # causes the test failed signal.
            measure_values = self.algorithm.get_measure(prob, self.test_id)
            if measure_values is None: # Some error in running the algorithm, 
                                       # so we could not get the meaure
                self.finalize()
                return TestResult(testIsFailed=True)
            #print measure_values
            if len(measure_values) == 0: # Some error in getting the measure, 
                                         # so we could not get the meaure
                self.finalize()
                return TestResult(testIsFailed=True) 
            self.measure_value_table.add_problem_measures(prob.name,measure_values)
        #print "ho ho test.py ",self.problems
        self.logger.log(str(self.measure_value_table))
        self.finalize()
        
        return TestResult(testIsFailed=False,
                          testNumber=self.test_number,
                          problems=self.problems,
                          parameters=self.parameters,
                          measureValueTable=self.measure_value_table)

    #def synchronize_measures(self):
    #    for i in range(len(self.measures)):
    #        tmp = self.measures[i]
    #        self.measures[i] = self.measures[i].get_global_object()
    #        del tmp
    #    # Resolve the link betwwen the measure functions and the value table
    #    return

    def log(self,fileName):
        self.logging.write(self,fileName)
    
    #def reduce_problem_set(self):
    #    newProblemSet = []
    #    i = 1
    #    for prob in self.problems:
    #        if i % 2 == 0:
    #            newProblemSet.append(prob)
    #        i = i + 1
    #    activeParameters = self.get_active_parameters()
    #    reducedData = ModelData(algorithm=self.algorithm,
    #                            problems=newProblemSet,
    #                            activeParameters=activeParameters,
    #                            platform=self.platform)
    #    return reducedData

        
        

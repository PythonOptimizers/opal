import os
import log
from measure import MeasureValueTable
from testproblem import TestProblem

from .. import config

class TestResult:

    def __init__(self, testIsFailed=None, testNumber=None, problems=None,
                 parameters=None, measureValueTable=None, **kwargs):

        self.test_is_failed = testIsFailed
        self.test_number = testNumber
        self.problems = problems
        self.parameters = parameters
        self.measure_value_table = measureValueTable
        return


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

    def __init__(self, algorithm, problems=None, parameters=None,
                 measures=None, platform=config.platform, logHandlers=[],
                 **kwargs):

        # The core variables
        self.algorithm = algorithm
        if (problems is None) or (len(problems) == 0):
            self.problems = [TestProblem(name='TESTPROB')]
        else:
            self.problems = problems

        if parameters is None:
            self.parameters = algorithm.parameters
        else:
            self.parameters = parameters

        if measures is None:
            self.measures = algorithm.measures
        else:
            self.measures = measures

        self.platform = platform

        self.logger = log.OPALLogger(name='ModelData', handlers=logHandlers)
        self.logger.log('Initializing ModelData object')
        self.test_number = 0
        self.test_id = None

        self.test_is_failed = False
        pNames = [prob.name for prob in self.problems]
        mNames = [measure.name for measure in self.measures]
        self.measure_value_table = MeasureValueTable(problem_names=pNames,
                                                     measure_names=mNames)
        return


    def get_parameters(self):

        self.logger.log('Requesting parameters')
        return self.parameters


    def initialize(self, parameterValues):
        """
        This method return an unique identity for the
        test basing on the parameter values

        The identity obtains by hashing the parameter values string.
        This is an inversable function. It means that we can get
        the parameter_values form the id
        """

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
        self.logger.log('Initializing test ' + str(self.test_number) + \
                         ' with id ' + str(self.test_id))
        self.logger.log(' - Parameter values: ' + valuesStr.replace('_', ' '))
        return


    def finalize(self):

        self.logger.log('Finalize the test ' + str(self.test_id))
        self.algorithm.clean_running_data(testId=self.test_id)
        return


    def run(self, parameterValues):

        self.initialize(parameterValues=parameterValues)

        self.logger.log('Running test ' + str(self.test_id))

        # Assign parameter values in algorithm and write to file.
        self.algorithm.set_parameter(parameters=self.parameters,
                                     testId=self.test_id)

        # Check feasibility.
        if not self.algorithm.are_parameters_valid():
            self.test_is_failed = True
            self.logger.log(' - Parameter values are invalid, ' + \
                             'test aborted')
            return

        # Launch algorithm.
        self.platform.initialize(self.test_id)
        self.logger.log(' - Solving test problems')
        for prob in self.problems:
            self.platform.execute(\
                self.algorithm.get_full_executable_command(problem=prob,
                                                           testId=self.test_id))

        resultIsReady = "numended(/g" + self.test_id + ", *)"
        self.platform.waitForCondition(resultIsReady)
        self.logger.log(' - All problems solved, test stopped')
        return


    def get_test_result(self):

        self.logger.log('Collecting test results')
        if self.test_is_failed is True:
            self.finalize()
            return TestResult(testIsFailed=True)

        for prob in self.problems:
            # We accept only a perfect measure values table, this means the
            # atomic measure are get from all of the problems. Any error
            # causes the test failed signal.
            measure_values = self.algorithm.get_measure(prob, self.test_id)
            if measure_values is None: # Error occurred
                self.finalize()
                return TestResult(testIsFailed=True)

            if len(measure_values) == 0: # Some error in getting the measure,
                self.finalize()
                return TestResult(testIsFailed=True)

            self.measure_value_table.add_problem_measures(prob.name,
                                                          measure_values)
        self.logger.log(str(self.measure_value_table))
        self.finalize()

        return TestResult(testIsFailed=False,
                          testNumber=self.test_number,
                          problems=self.problems,
                          parameters=self.parameters,
                          measureValueTable=self.measure_value_table)


    def log(self,fileName):
        self.logging.write(self, fileName)

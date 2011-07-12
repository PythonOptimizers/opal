import copy
import os

from opal.core.parameter import Parameter, ParameterConstraint
from opal.core.data import DataSet
from opal.core.measure import Measure
import log

__docformat__ = 'restructuredtext'

class Algorithm:
    """
    An abstract class to define the specifics of an algorithm.

    :parameters:
        :name:  Name of the algorithm (string)
        :purpose: Synopsis of purpose (string)

    Each algorithm has two aspect:

     1. Algorithmic aspect: the name, purpose, parameters, measures and the
        constraints on the parameters. The measures represent the output of the
        alorithm.

     2. Computational aspect: the description of how to run algorithm and what
        the output is.

    Example:

      >>> dfo = Algorithm(name='DFO', purpose='Derivative-free optimization')
      >>> delmin = Parameter(default=1.0e-3, name='DELMIN')
      >>> dfo.add_param(delmin)
      >>> maxit = Parameter(type='integer', default=100, name='MAXIT')
      >>> dfo.add_param(maxit)
      >>> cpuTime = Measure(type='real', name='TIME')
      >>> dfo.add_measure(cpuTime)
      >>> print [param.name for param in dfo.parameters]
      ['DELMIN', 'MAXIT']
      >>> real_params = [param for param in dfo.parameters if param.is_real]
      >>> print [param.name for param in real_params]
      ['DELMIN']
    """

    def __init__(self, name=None, description=None, logHandlers=[], **kwargs):

        # Algorithmic description
        self.logger = log.OPALLogger(name='Algorithm',
                                     handlers=logHandlers)

        self.name = name
        self.description = description
        self.parameters = DataSet(name='Parameter set')
        self.measures = DataSet(name='Measure set')
        self.constraints = []

        # Computational description
        self.parameter_file = self.name + '.param'
        self.parameter_writing_method = None
        self.measure_reading_method = None
        self.executable = None
        self.neighbors_executable = None
        self.logger.log('Initializing Algorithm %s' % self.name)
        return


    def add_param(self, param):
        "Register a new parameter with an algorithm"

        if isinstance(param, Parameter):
            self.logger.log('Registering parameter %s (%s)' % (param.name,
                                                               param.kind))
            self.parameters.append(param)
        else:
            raise TypeError, 'param must be a Parameter'
        return


    def add_measure(self, measure):
        "Register a new measure with an algorithm"

        if isinstance(measure, Measure):
            self.logger.log('Registering measure %s' % measure.name)
            self.measures.append(measure)
        else:
            raise TypeError, 'measure must be a Measure object'
        return


    def set_executable_command(self, executable):

        self.logger.log('Setting executable command to %s' % executable)
        self.executable = executable
        return


    def set_neighbors_command(self, executable):

        self.logger.log('Setting executable command for neighbors to %s' % \
                executable)
        self.neighbors_executable = executable
        return


    def set_parameter_file(self, parameter_file, writing_method=None):
        """
        Parameter values are set via file IO.
        This method assigns the parameter file name to be use throughout the
        optimization process. The `writing_method` argument
        represent the file format. By default, `writing_method` is
        set to the `set_parameter_value()` method. In this case, the parameters
        are dumped to a file named `parameter_file`.
        If parameter_file is None, the parameter values
        are transmitted to the executable driver as the arguments
        `writing_method` must have the form writing_method(algo, parameters)
        where `algo` is an Algorithm instance.
        """

        self.logger.log('Setting parameter file name to %s' % parameter_file)
        self.parameter_file = parameter_file
        self.parameter_writing_method = copy.copy(writing_method)
        return


    def set_measure_file(self, measure_file=None, reading_method=None):
        """
        An executable algorithm has two choices for outputting
        the measure values:

         1. to screen (`measure_file` is None). In this case, the output is
            also redirected to a file named after the algorithm and problem
            being solved, for example DFO-HS1.out.

         2. to a file named `measure_file`.

        The `reading_method` argument specifies how to extract the measure
        values from the output of the algorithm.
        """

        self.logger.log('Setting measure file name to %s' % measure_file)
        self.measure_file = measure_file
        self.measure_reading_method = reading_method
        return


    def set_parameter(self, parameters, testId=''):
        """
        This method return an unique identity for the
        test basing on the parameter values

        The identity obtains by hashing the parameter values string.
        This is an inversable function. It means that we can get
        the parameter_values form the id

        This virtual method determines how values for the parameters of the
        algorithm are written to intermediated file that are read after by
        algorithm driver.

        The format of intermediated file depend on this method. By default,
        the parameter set are written by pickle.
        """

        self.logger.log('Assigning parameter values and writing to file')

        # Fill the values to parameter set
        j = 0
        for i in range(len(parameters)):
            if self.parameters[i].name == parameters[j].name:
                self.parameters[i].set_value(parameters[j].value)
                j = j + 1

        # Write the values to a temporary parameter file
        # for communicating with an executable wrapper
        if self.parameter_writing_method is not None:
            self.parameter_writing_method(self)
        else:
            paramFileName = self.get_parameter_file(testId=testId)
            f = open(paramFileName, 'w')
            for p in self.parameters:
                s = p.name + ':' +  p.kind + ':' + str(p.value) + '\n'
                f.write(s)
            f.close()
        return


    def get_parameter_file(self, testId=''):
        "Return parameter file name."

        self.logger.log('Requesting parameter file name')
        return self.name + '_' + testId + '.param'


    def get_measure_file(self, problem, testId=''):
        "Return measure file name."

        self.logger.log('Requesting measure file name')
        return self.name + '_' + problem.name + '_' + testId + '.out'


    def get_measure(self, problem, testId):
        """
        Ths virtual method determines how to measure value from the
        output of the algorithm.

        :parameters:
            :problem:
            :testId:

        :returns: A mapping measure name --> measure value

        By default, the algorithm returns the measure values to the standard
        output. In the `run()` method, the output is redirected to file.
        """

        self.logger.log('Gathering measures from output of algorithm')

        if self.measure_reading_method is not None:
            return self.measure_reading_method(self, problem)
        measureFile = self.get_measure_file(problem=problem, testId=testId)
        f = open(measureFile)
        lines = f.readlines()
        f.close()
        os.remove(measureFile)
        converters = {'categorical':str, 'integer':int, 'real':float}
        measure_values = {}
        for line in lines:
            line.strip('\n')
            if len(line) < 1: continue
            fields = line.split(' ')
            if len(fields) < 2: continue
            measure_values[fields[0].strip(' ')] = fields[1].strip(' ')
        for i in range(len(self.measures)):
            convert = converters[self.measures[i].get_type()]
            try:
                measure_values[self.measures[i].name] = \
                    convert(measure_values[self.measures[i].name])
            except ValueError:
                return None # error occurred

        return measure_values


    def get_full_executable_command(self, problem, testId=''):
        """
        .. warning::

            What kind of object is `problem`???

        This virtual method determines how to run the algorithm.

        :parameters:
            :problem: Problem (???)

        :returns: The command for executing the algorithm.

        By default, the algorithm is called by the command

            `./algorithm paramfile problem`
        """

        self.logger.log('Requesting complete executable command')
        outputFile = self.get_measure_file(problem=problem, testId=testId)
        paramFile = self.get_parameter_file(testId=testId)
        cmd = ' '.join([self.executable, paramFile, problem.name, outputFile])
        return cmd


    def clean_running_data(self, testId=''):

        self.logger.log('Cleaning up parameter file')
        paramFile = self.get_parameter_file(testId=testId)
        if os.path.exists(paramFile):
            os.remove(paramFile)
        return


    def add_parameter_constraint(self, paramConstraint):
        "Register a new simple constraint on a parameter."

        self.logger.log('Registering simple constraint')
        if isinstance(paramConstraint, ParameterConstraint):
            self.constraints.append(paramConstraint)
        elif isinstance(paramConstraint, str):
            self.constraints.append(ParameterConstraint(paramConstraint))
        else:
            msg = 'paramConstraint must be a String or ParameterConstraint'
            raise TypeError, msg
        return


    def are_parameters_valid(self):
        """
        Return True if all parameters are in their domain and satisfy the
        constraints. Return False otherwise.
        """

        self.logger.log('Checking if parameters satisfy constraints')
        for constraint in self.constraints:
            if constraint(self.parameters) is ParameterConstraint.violated:
                return ParameterConstraint.violated
        for param in self.parameters:
            if not param.is_valid():
                return False
        return True


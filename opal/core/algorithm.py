import pickle
import copy
import os

from .parameter import Parameter
from .parameter import ParameterConstraint
from .measure import Measure

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

    def __init__(self, name=None, purpose=None, **kwargs):
       
        # Algorithmic description
        self.name = name
        self.purpose = purpose
        self.parameters = [] # List of parameters (of type Parameter)
        self.measures = [] # List of measures (the output of the algorithm)
        self.constraints = []

        # Computational description
        self.parameter_file = None
        self.parameter_writing_method = None
        self.measure_reading_method = None
        self.executable = None

    def add_param(self, param):
        "Add a parameter to an algorithm"
        if isinstance(param, Parameter):
            self.parameters.append(param)
        else:
            raise TypeError, 'param must be a Parameter'
        return
    
    def add_measure(self, measure):
        "Add a measure to an algorithm"
        if isinstance(measure, Measure):
            self.measures.append(measure)
        else:
            raise TypeError, 'measure must be a Measure object'
        return

    def set_executable_command(self,executable):
        self.executable = executable
        return

    def set_parameter_file(self, parameter_file, writing_method=None):
        """
        Parameter values are set via file IO.
        This method assigns the parameter file name to be use throughout the
        optimization process. The `writing_method` argument
        represent the file format. By default, `writing_method` is
        set to the `set_parameter_value()` method. In this case, the parameters
        are dumped to a file named `parameter_file` using `pickle.dump()`.
        If parameter_file is None, the parameter values 
        are transmitted to the executable driver as the arguments
        `writing_method` must have the form writing_method(algo, parameters)
        where `algo` is an Algorithm instance.
        """
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
        self.measure_file = measure_file
        self.measure_reading_method = reading_method
        return

    def set_parameter(self, parameters):
        """
        This virtual method determines how values for the parameters of the
        algorithm are set. Some algorithms set values through file, others
        directly by argument.

        :parameters:
            :parameters: List of parameter whose values are set.
        """
        if self.parameter_writing_method is not None:
            self.parameter_writing_method(self, parameters)
        else:
            f = open(self.parameter_file, 'w')
            pardict = {}
            for param in parameters:
                pardict[param.name] = param
            pickle.dump(pardict, f)
            f.close()
        return
    
    def get_output(self):
        return 'file'

    def get_measure_file(self, problem):
        "Return measure file name."
        return self.name + '-' + problem.name + '.out'

    def get_measure(self, problem, measures):
        """
        Ths virtual method determines how to extract a measure value from the
        output of the algorithm.

        :parameters:
            :problem:
            :measures: List of measures we want to extract

        :returns: A mapping measure name --> measure value

        By default, the algorithm returns the measure values to the standard
        output. In the `run()` method, the output is redirected to file.
        """
        if self.measure_reading_method is not None:
            return self.measure_reading_method(self, problem, measures)
        #allValues = []
        #allValues = {}
        measureFile = self.name + '-' + problem.name + '.out' 
        f = open(measureFile)
        #map(lambda l: allValues.extend(l.strip('\n').strip(' ').split(' ')), f.readlines())
        #valueStr = f.read()
        lines = f.readlines()
        f.close()
        os.remove(measureFile)
        converters = {'categorical':str, 'integer':int, 'real':float}
        measure_values = {}
        for line in lines:
            line.strip('\n')
            if len(line) < 1:
                continue
            fields = line.split(' ')
            if len(fields) < 2:
                continue
            measure_values[fields[0].strip(' ')] = fields[1].strip(' ')
        for i in range(len(measures)):
            measure_values[measures[i].name] = converters[measures[i].kind](measure_values[measures[i].name])
        #print '[algorithm.py]', allValues, [measure.name for measure in measures]
        # measure_values = eval(valueStr)
        #print 'print in algorithm.py',measure_values
        return measure_values

    def get_full_executable_command(self, paramValues, problem):
        """
        .. warning::

            Why do we need `paramValues` here???
            What kind of object is `problem`???

        This virtual method determines how to run the algorithm.

        :parameters:
            :paramValues: List of parameter values
            :problem: Problem (???)

        :returns: The command for executing the algorithm.

        By default, the algorithm is called by the command 

            `./algorithm paramfile problem`
        """
        cmd = self.executable + ' ' + self.parameter_file + ' ' + problem.name
        return cmd

    def add_parameter_constraint(self, paramConstraint):
        """
        Specify the domain of a parameter.
        """
        if isinstance(paramConstraint, ParameterConstraint):
            self.constraints.append(paramConstraint)
        elif isinstance(paramConstraint, str):
            self.constraints.append(ParameterConstraint(paramConstraint))
        else:
            msg = 'paramConstraint must be a String or ParameterConstraint'
            raise TypeError, msg
        return

    def are_parameters_valid(self, parameters):
        """
        Return True if all parameters are in their domain and satisfy the
        constraints. Return False otherwise.
        """
        #print '[algorithm.py]',[param.value for param in parameters]
        for constraint in self.constraints:
            if constraint(parameters) is ParameterConstraint.violated:
                return ParameterConstraint.violated
        for param in parameters:
            if not param.is_valid():
                return False
        return True
    

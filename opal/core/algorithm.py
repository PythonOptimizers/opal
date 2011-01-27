#import pickle
import copy
import os

from opal.core.parameter import Parameter, ParameterConstraint
from opal.core.measure import Measure

__docformat__ = 'restructuredtext'
  
class AlgorithmWrapper:
    """
    
    An abstract class to define the specifics of a wrapper of an algorithm. 
    An object of this class represent to an executable 
    wrapper of target algorithm. It provoke the target
    algorithm to solve a problem and collect the elementary
    measures

    An object of this class works as an interface of the target algorithm 
    with OPAL. It contains at least three informations:
    
    1. What are the parammeters
    2. How to invoke the algorithm to solve a problem
    3. What are the measures we get after running algorithm

    
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
        self.parameter_file = self.name + '.param'
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

    def set_executable_command(self, executable):
        self.executable = executable
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
            for param in self.parameters:
                f.write(param.name + ':' +  param.kind + ':' + str(param.value) + '\n')
            f.close()
        return 
    
    def get_output(self):
        return 'file'

    def get_parameter_file(self, testId=''):
        return self.name + '_' + testId + '.param'

    def get_measure_file(self, problem, testId=''):
        "Return measure file name."
        return self.name + '_' + problem.name + '_' + testId + '.out' 

    def get_measure(self, problem, testId):
        """

        Ths virtual method determines how to  measure value from the
        output of the algorithm.

        :parameters:
            :problem:
            :measures: List of measures we want to extract

        :returns: A mapping measure name --> measure value

        By default, the algorithm returns the measure values to the standard
        output. In the `run()` method, the output is redirected to file.
        """
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
            if len(line) < 1:
                continue
            fields = line.split(' ')
            if len(fields) < 2:
                continue
            measure_values[fields[0].strip(' ')] = fields[1].strip(' ')
        for i in range(len(self.measures)):
            kind = converters[self.measures[i].kind]
            try:
                measure_values[self.measures[i].name] = \
                    kind(measure_values[self.measures[i].name])
            except ValueError:
                return None # Return a signal indicating that certain error occurs
                #raise Exception('Error in tranform ' + \
                #                    measure_values[self.measures[i].name] + ' to ' + \
                #                    self.measures[i].name + ' in ' +\
                #                    measureFile + ': ' + line)

        return measure_values

    def get_full_executable_command(self, problem, testId=''):
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
        outputFile = self.get_measure_file(problem=problem, testId=testId)
        paramFile = self.get_parameter_file(testId=testId)
        #if outputFile == 'STDOUT': # algorithm wrapper will output the measure value to screen
        cmd = self.executable + ' ' + paramFile + ' ' + problem.name + ' ' + outputFile 
        return cmd

    def clean_running_data(self, testId=''):
        paramFile = self.get_parameter_file(testId=testId)
        if os.path.exists(paramFile):
            os.remove(paramFile)
        return
    
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

    def are_parameters_valid(self):
        """
        Return True if all parameters are in their domain and satisfy the
        constraints. Return False otherwise.
        """
        #print '[algorithm.py]',[param.value for param in parameters]
        for constraint in self.constraints:
            if constraint(self.parameters) is ParameterConstraint.violated:
                return ParameterConstraint.violated
        for param in self.parameters:
            if not param.is_valid():
                return False
        return True
    

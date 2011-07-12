#import pickle
import copy
import os
import tempfile

from data import DataSet
from parameter import Parameter, ParameterConstraint
from measure import Measure


__docformat__ = 'restructuredtext'
  
class Algorithm:
    """
    
    An abstract class to define the specifics of a wrapper of an algorithm. 
    An object of this class represents to an executable 
    wrapper of target algorithm. It provokes the target
    algorithm to solve a problem and collects the elementary
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

    def __init__(self, name=None, description=None, **kwargs):
       
        # Algorithmic description
        self.name = name
        self.description = description
        self.parameters = DataSet(name='Parameter set')  # List of parameters 
                                                         # (of type Parameter)
        self.measures = DataSet(name='Measure set')  # List of measures 
                                                     # (the observation of the 
                                                     # algorithm)
        self.constraints = []

        # Computational description
        self.parameter_file = self.name + '.param'
        self.sessions = {} # dictionary map between session id and parameter
                           # values

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

   
    def update_parameters(self, parameters):
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
        values = dict((param.name,param.value) for param in parameters)
        # Fill the values to parameter set
        self.parameters.set_values(values)
        # Write the values to a temporary parameter file 
        # for communicating with an executable wrapper 
        return 
    

    def create_tag(self, problem):
        return 

    def set_executable_command(self, command):
        self.executable = command
        return

    def write_parameter(self, fileName):
        f = open(fileName, 'w')
        for param in self.parameters:
            f.write(param.name + ':' +  param.kind + ':' + \
                    str(param.value) + '\n')
        f.close()
        return

    def read_measure(self, fileName):
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
        
        f = open(fileName)
        lines = f.readlines()
        f.close()
        converters = {'categorical':str, 'integer':int, 'real':float}
        measure_values = {}
        for line in lines:
            line.strip('\n')
            if len(line) < 1:
                continue
            fields = line.split(' ')
            if len(fields) < 2:
                continue
            measureName = fields[0].strip(' ')
            if measureName not in self.measures:
                continue
            measure_values[measureName] = fields[1].strip(' ')
        for i in range(len(self.measures)):
            convert = converters[self.measures[i].get_type()]
            try:
                measure_values[self.measures[i].name] = \
                    convert(measure_values[self.measures[i].name])
            except ValueError:
                return None
        return measure_values

    def solve(self, problem, parameters=None, parameterTag=None ):
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
        
        if parameters is not None:
            self.update_parameters(parameters)

        if parameterTag is not None:
            sessionTag = problem.name + '_' + parameterTag
        else:
            sessionTag = self.create_tag(problem)
            
        parameterFile = self.name + '_' +\
                        str(sessionTag) +\
                        '.param'
                                                        
        outputFile = self.name + '_' +\
                     str(sessionTag) +\
                     '.measure'

        if not os.path.exists(parameterFile):
            self.write_parameter(parameterFile)
        cmd = self.executable + ' ' +\
              parameterFile + ' ' +\
              problem.name + ' ' +\
              outputFile        
       
            
        return cmd, parameterFile, outputFile, sessionTag

    
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
    

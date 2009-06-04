from .parameter import Parameter
from .parameter import ParameterConstraint
from .driver import Driver

  
class Algorithm:
    """
    An abstract class to gather the parameters of an algorithm. Example:

      >>> dfo = Algorithm(name='DFO', purpose='Derivative-free minimization')
      >>> delmin = Parameter(default=1.0e-3, name='DELMIN')
      >>> dfo.add_param(delmin)
      >>> mxit = Parameter(type='integer', default=100, name='MAXIT')
      >>> dfo.add_param(mxit)
      >>> print [param.name for param in dfo.parameters]
      ['DELMIN', 'MAXIT']
      >>> real_params = [param for param in dfo.parameters if param.is_real]
      >>> print [param.name for param in real_params]
      ['DELMIN']
    """

    def __init__(self, name=None, purpose=None,**kwargs):

        self.name = name
        self.purpose = purpose
        self.parameters = [] # List of parameters (of type Parameter)
        self.constraints = []
        self.parameter_file = None
        self.executable = None

    def add_param(self, param):
        "Add a parameter to an algorithm"
        if isinstance(param, Parameter):
            self.parameters.append(param)
        else:
            raise TypeError, 'param must be a Parameter'
        return
    
    def set_executable(self,executable):
        self.executable = executable
        return

    def set_parameter_file(self,parameter_file):
        self.parameter_file = parameter_file
        return

    def set_parameter_values(self,parameters):
        # The virtual method determines how to
        # set values for the parameters of the algorithm
        # The way to set values depends from the algorithm
        # Some algorithms set values through the file, the 
        # others set directly by the program argument
        # This method is realized in the class of a specific 
        # algorithm
        # Input: list of parameter whose values are set
        # Output: void
        f = open(self.parameter_file,'w')
        for param in parameters:
            print >> f, param.export_to_dict()
        f.close()
        return
    
    def get_measure(self,problemName,measures):
        # The virtual method determines how to 
        # extract the measure value from the running result
        # Input: List of measures we want to get
        # Output: A mapping measure name --> measure value
        # By default, the algorithm will return 
        # the measure values to the standard output
        # In the run() method, we will redirect the output
        # to the file, say, ALGORITHM-PROBLEM.out
        allValues = []
        f = open(self.name + '-' + problemName + '.out')
        map(lambda l: allValues.extend(l.split(' ')), f.readlines())
        f.close()
        
        measure_values = {}
        converters = {'categorical':str,'integer':int,'real':float}
        for i in range(len(measures)):
            measure_values[measures[i].name] = converters[measures[i].kind](allValues[i])
        return measure_values

    def get_call_cmd(self,paramValues=None,problem=None):
        # The virtual method determines how to
        # run algorithm
        # Input: List of parameter values
        #        Problem
        # Output: The command for executing the algorithm
        # By default, we assume that the algorithm is called by
        # the command 
        # ./algorithm paramfile problem
        output_file_name = self.name + '-' + problem + '.out'
        executingCmd = self.executable + ' ' + self.parameter_file + ' ' + problem + ' > ' +  output_file_name
        return executingCmd

    def add_parameter_constraint(self, paramConstraint):
        if isinstance(paramConstraint,ParameterConstraint):
            self.constraints.append(paramConstraint)
        elif isinstance(paramConstraint,str):
            self.constraints.append(ParameterConstraint(paramConstraint))
        else:
            raise TypeError, 'Parameter Constraint is a String or ParameterConstraint'
        return

    def verify(self,parameterValues):
        for constraint in self.constraints:
            if constraint(parameterValues) is ParameterConstraint.violated:
                return ParameterConstraint.violated
        return not ParameterConstraint.violated
    

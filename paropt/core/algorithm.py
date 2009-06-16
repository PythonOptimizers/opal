import pickle
from .parameter import Parameter
from .parameter import ParameterConstraint
from .measure import Measure
  
class Algorithm:
    """
    An abstract class to gather the parameters of an algorithm. 
    Each algorithm has two aspect:
     - Algorithmic aspect: this is the description about the name, purpose, parameters, measures and the constraints 
       on the parameters. The measures represent for the algorithm's output
     - Computational aspect: this is the description how to run algorithm and what is the output
    Example:

      >>> dfo = Algorithm(name='DFO', purpose='Derivative-free minimization')
      >>> delmin = Parameter(default=1.0e-3, name='DELMIN')
      >>> dfo.add_param(delmin)
      >>> mxit = Parameter(type='integer', default=100, name='MAXIT')
      >>> dfo.add_param(mxit)
      >>> cpuTime = Measure(type='real',name='TIME')
      >>> dfo.add_measure(cpuTime)
      >>> print [param.name for param in dfo.parameters]
      ['DELMIN', 'MAXIT']
      >>> real_params = [param for param in dfo.parameters if param.is_real]
      >>> print [param.name for param in real_params]
      ['DELMIN']
    """

    def __init__(self, name=None, purpose=None,**kwargs):
       
        # Algorithmic description
        self.name = name
        self.purpose = purpose
        self.parameters = [] # List of parameters (of type Parameter)
        self.measures = [] # List of measures (the output of the algorithm)
        self.constraints = []
        # Computational description
        self.parameter_file = None
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

    def set_executable(self,executable):
        self.executable = executable
        return

    def set_parameter_file(self,parameter_file,writting_method=None):
        # We consider that the parameter value setting is done through file
        # This method is to set parameter file name. The writting_method 
        # represent for the file format. In the default case, writting_method is
        # set to the set_parameter_value() method. In this case, the parameters are 
        # dump to a file named by parameter_file by pickle.dump() method
        # if parameter_file is set to None, we consider that the parameter values 
        # are transmitted to the executable driver as the arguments
        self.parameter_file = parameter_file
        if writting_method is not None:
            self.set_parameter_values = writting_method
        return

    def set_measure_file(self,measure_file=None,reading_method=None):
        # We consider that an executable algorithm has two choices for outputing  
        # whose content contains the measure values:
        #  1 - Output the screen, measure_file is None, the output is indirected 
        #      to a file named by paropt, for example DFO-HS1.out
        #  2 - Output to a file whose name is specified by measure_file. The measure_file
        #      may be the naming rule like ABC-[problem]-output.txt.
        # reading_method specifies how to extract the measure values from the output
        self.measure_file = measure_file
        if reading_method is not None:
            self.get_measure = reading_method
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
        pardict = {}
        for param in parameters:
            pardict[param.name] = param
        pickle.dump(pardict, f)
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
        map(lambda l: allValues.extend(l.strip('\n').split(' ')), f.readlines())
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

    def are_parameters_valid(self,parameters):
        for constraint in self.constraints:
            if constraint(parameters) is ParameterConstraint.violated:
                return ParameterConstraint.violated
        for param in parameters:
            if not param.is_valid():
                return False
        return True
    

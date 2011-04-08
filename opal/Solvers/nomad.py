import sys
import os
import logging
import pickle

from ..core.model import Model
from ..core.solver import Solver
from ..core.mafrw import Agent
from ..core.mafrw import Message

from ..core.mafrw import Environment

from opal import ModelEvaluator
#from ..core.blackbox import BlackBox

__docformat__ = 'restructuredtext'

class NOMADSpecification:
    "Used to specify black-box solver options."

    def __init__(self,name=None,value=None,**kwargs):
        self.name = name
        self.value = value
        pass

    def str(self):
        if (self.name is not None) and (self.value is not None):
            return self.name + ' ' + str(self.value)
        return ""

class NOMADCommunicator(Agent):
    '''

    This class encapsulates methods of communication between
    NOMAD solver and an executable blackbox.
    It handles two messages:

    - Input message whose content contains the name of input file. 
      The point coordinates will be extracted from the file and are
      used to form an evaluation request
    - Output message whose content contains the model values. There 
      values are shown up to the standard output as expectation of 
      NOMAD solver
    '''

    def __init__(self, name='nomad blackbox communicator',
                 logHandlers=[],
                 input=None, output=None):
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        self.inputFile = input
        self.outputStream = output
        self.message_handlers['inform-model-value'] = self.write_output
        return
    
    def read_input(self, inputFile=None):
        """
        .. warning::

            Document this method!!!
        """
        inputValues = []
        #print args
        #print ""
        if inputFile is None:
            return inputValues

        # Extract every words from the file and save to a list
        f = open(inputFile)
        map(lambda l: inputValues.extend(l.strip('\n').strip(' ').split(' ')),
                                         f.readlines())
        f.close()
        return inputValues

    def write_output(self, info):
        """

        Message handlers that write the values obtained by the model-value
        informing message in the understandable order specified by NOMAD
        blackbox
        """
        objValue, consValues = info['proposition']['values']
        self.outputStream.write(str(objValue) + '\n')
        
        # Constraint values are list of tuple
        # (left_size_value, right_size_value) values that computed from a 
        # constraint of form
        #   left_bound <= f(x) <= right_bound
        # by following rule:
        #   left_size_value = left_bound - f(x)
        #   right_size_value = f(x) - right_bound
        # So in the desired form of NOMAD (g(x) <= 0), each tuple of constraint
        # value is written as two constraints:
        #   left_bound - f(x) <= 0, and  f(x) - right_bound <=0
        for cons in consValues:
            if cons[0] is not None:
                self.outputStream.write(str(cons[0]) + ' ')
            if cons[1] is not None:
                self.outputStream.write(str(cons[1]))
        self.outputStream.write('\n')
        return

    def  run(self):
        if self.inputFile is not None:
            inputValues = self.read_input(inputFile=self.inputFile)
        msg = Message(performative='cfp',
                      sender=self.id,
                      receiver=None,
                      content={'action':'evaluate-point',
                               'proposition':{'point': inputValues}
                               })
        self.sent_request_id = self.send_message(msg)
        Agent.run(self)
        return
   

class NOMADBlackbox(Environment):
    """

    NOMADBlackbox object represent a NOMAD blackbox that is kind of an interface
    between the NOMAD solver and model (problem). Because of the fact that the 
    used NOMAD solver require that an blackbox is an executable with three 
    properties:
    
    #. Accept a file containing inputed point as only argument
    
    #. Evaluate model with the given point

    #. Show the model values to standard output

    we design in such a way that the executable will initialize an NOMADBlackbox 
    object too. The advantage that we minimize the generated code of the
    executable
    
    NOMADBlackbox object is an application that contains two agents: an 
    NOMADCommunicator worker and a ModelEvaluator broker. A session is 
    activated by sending a message to NOMADCommunicator worker and finished 
    as this NOMADCommunicator worker shows the model values
    """

    def __init__(self, 
                 name='nomad blackbox',
                 logHandlers=[],
                 model=None,
                 input=None,
                 output=None):
        # Initialize agents
        Environment.__init__(self, name=name, logHandlers=logHandlers)
        self.communicator = NOMADCommunicator(name='communicator',
                                              input=input, 
                                              output=output)
        self.evaluator = ModelEvaluator(name='evaluator', modelFile=model)
        # Register the agnets
        self.communicator.register(self)
        self.evaluator.register(self)
        return
            

    def run(self):
        self.logger.log('Begin of a session')
        self.initialize()
        # Wait the comnunicator finishes its work. This happends when 
        # the communicator get a message containing the model values 
        # (evaluator replies)
        self.communicator.join(30)
        self.finalize()
        self.logger.log('End of a session')
        return 
   
    

 

class NOMADSolver(Solver):
    """
    An instance of the abstract Solver class.
    A NOMADSolver object specifies the particulars of the NOMAD direct search
    solver for black-box optimization.
    For more information about the NOMAD, see `http://wwww.gerad.ca/NOMAD`_.
    """

    def __init__(self, name='NOMAD', parameterFile='nomad-param.txt', **kwargs):
        Solver.__init__(self, name='NOMAD', **kwargs)
        self.paramFileName = parameterFile
        self.resultFileName = 'nomad-result.txt'
        self.solutionFileName = 'nomad-solution.txt'
        self.blackbox = None
        self.surrogate = None
        self.parameter_settings = [] # List of line in parameter file
        return

    def solve(self, model=None, surrogate=None):
        '''

        The solving process consist of three steps:

        #. Generate the executable to evaluate model
        
        #. Generate the specification corresponding model

        #. Execute command nomad with the generated specificaton file
        '''
        #self.blackbox = NOMADBlackbox(model=model)
        #self.blackbox.generate_executable_file()
        self.generate_blackbox_executable(model=model,
                                          execFile='blackbox.py',
                                          dataFile='blackbox.dat')
        if surrogate is not None:
            self.generate_blackbox_executable(model=surrogate,
                                              execFile='surrogate.py',
                                              dataFile='surrogate.dat')
        #   surrogate.save()
        self.create_specification_file(model=model,
                                       modelExecutable='$python  blackbox.py', 
                                       surrogate=surrogate,
                                       surrogateExecutable=\
                                       '$python surrogate.py')
        
        self.run()
        return

    def generate_blackbox_executable(self,
                                     model,
                                     execFile='blackbox.py',
                                     dataFile='blackbox.dat'):
        """
        
        Generate Python code to play the role of black box executable.
        """

        tab = ' '*4
        endl = '\n'
        comment = '# '
        bb = open(execFile, 'w')
        # Import the neccessary modules
        bb.write('import os' + endl)
        bb.write('import sys' + endl)
        bb.write('import string' + endl)
        bb.write('import shutil' + endl)
        bb.write('import pickle' + endl)
        bb.write('import logging' + endl)
        bb.write('from opal.Solvers.nomad import NOMADBlackbox' + endl)
        bb.write('from opal.core.modelevaluator import ModelEvaluator' + endl)
        bb.write(comment + 'Create model evaluation environment' + endl)
        bb.write('env = NOMADBlackbox(model="' + dataFile + \
                 '",input=sys.argv[1], output=sys.stdout)' + endl)
        bb.write(comment + 'Activate the environment' + endl)
        bb.write('env.start()')
        bb.write(comment + 'Wait for environement finish his life time' + endl)
        bb.write('env.join()' + endl)
        bb.close()
        
        # Dump model to the file so that the executable blackbox can load it as
        # blackbox data

        f = open(dataFile, 'w')
        pickle.dump(model, f)
        f.close()
        return
    
    def create_specification_file(self, 
                                  model=None,
                                  modelExecutable=None,
                                  surrogate=None,
                                  surrogateExecutable=None):
        "Write NOMAD config to file based on parameter optimization problem."

        if model is None:
            return
        
        descrFile = open(self.paramFileName, "w")
        
        descrFile.write('DIMENSION ' + str(model.get_n_variable()) + '\n')
            # descrFile.write('DISPLAY_DEGREE 4\n')
        descrFile.write('DISPLAY_STATS EVAL BBE [ SOL, ] OBJ TIME \\\\\n')
        descrFile.write('BB_EXE "' + modelExecutable + '"\n')
        bbTypeStr = 'BB_OUTPUT_TYPE OBJ'
        for i in range(model.get_n_constraints()):
            bbTypeStr = bbTypeStr + ' PB'
        descrFile.write(bbTypeStr + '\n')
        #surrogate = self.surrogate
        if self.surrogate is not None:
            descrFile.write('SGTE_EXE "' + surrogateExecutable + '"\n')
        pointStr = str(model.initial_point)
        descrFile.write('X0 ' +  pointStr.replace(',',' ') + '\n')
        if model.bounds is not None:
            lowerBoundStr = str([bound[0] for bound in model.bounds \
                                     if bound is not None])\
                                     .replace('None','-').replace(',',' ')
            upperBoundStr = str([bound[1] for bound in model.bounds \
                                     if bound is not None])\
                                     .replace('None','-').replace(',',' ')
            if len(lowerBoundStr.replace(']','').replace('[','')) > 1:
                descrFile.write('LOWER_BOUND ' + lowerBoundStr + '\n')
            if len(upperBoundStr.replace(']','').replace('[','')) > 1:
                descrFile.write('UPPER_BOUND ' + upperBoundStr + '\n')
        # Write other settings.
        descrFile.write('SOLUTION_FILE ' + self.solutionFileName + '\n')
        descrFile.write('STATS_FILE ' + self.resultFileName + \
                ' $EVAL$ & $BBE$ &  [ $SOL$ ] & $OBJ$ & $TIME$ \\\\\n')
        for param_setting in self.parameter_settings:
            descrFile.write(param_setting + '\n')
        descrFile.close()
        return

    def set_parameter(self, name=None, value=None):
        param = NOMADSpecification(name=name,value=value)
        self.parameter_settings.append(param.str())
        return

    def run(self):
        os.system('nomad ' + self.paramFileName)
        return

class NOMADMPISolver(NOMADSolver):
    def __init__(self,
                 name='NOMAD.MPI',
                 parameterFile='nomad.mpi-param.txt',
                 np=None,
                 **kwargs):
        NOMADSolver.__init__(self, name=name, parameterFile=parameterFile)
        self.mpi_config = {}  # Contains the settings for MPI environment
        self.mpi_config['np'] = None  # If set this to None, the number
                                      # process is
                                      # determined idealy by the dimension of
                                      # solving problem.
        return

    def set_mpi_config(self, name, value):
        self.mpi_config[name] = value
        return

    def run(self):
        optionStr = ''
        for opt in self.mpi_config.keys():
            optionStr = ' -' + opt + ' ' + str(self.mpi_config[opt])
        os.system('mpirun' + optionStr + ' ' + \
                      'nomad.MPI ' + self.paramFileName)
        return

NOMAD = NOMADSolver()
NOMADMPI = NOMADMPISolver()

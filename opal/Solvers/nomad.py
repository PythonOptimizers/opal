import sys
import os
import logging
from ..core.solver import Solver
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


class NOMADBlackbox(ModelEvaluator):
    """

    NOMADBlackbox contains
    the description and the method of communication between
    NOMAD solver and an executable blackbox.

    In other words, NOMAD blackbox is a specific model evaluator that has two:
    particularities:
    - Executed as an external executable
    - Inputet by a file, outputs to standard output with a list of values of 
      functions (objective and constraints).
    The executable is created to communicate with NOMAD has 
    - the I/O stubs obey NOMAD's IO rule: input is a file, output to screen.
    - Initialize the agents (worker and broker): DataGenerator, 
      StructureComputer
   

    The descriptions include the executable file name
    The communicating methods are read_input and write_output
    Those are specialized to NOMAD solver
    """

    def __init__(self, model=None, fileName='blackbox.py',
                 **kwargs):

        #BlackBox.__init__(self, solver=solver, model=model, **kwargs)
        self.model=model
        self.file_name = fileName
        #self.surrogate = None
        pass

    def read_input(self, inputFile=None):
        """
        .. warning::

            Document this method!!!
        """
        inputValues = []
        paramValues = []
        #print args
        #print ""
        if inputFile is None:
            return (inputValues, paramValues)

        # Extract every words from the file and save to a list
        f = open(inputFile)
        map(lambda l: inputValues.extend(l.strip('\n').strip(' ').split(' ')),
                                         f.readlines())
        f.close()
        return (inputValues, paramValues)

    def write_output(self, objectiveValue, constraintValues):
        """
        .. warning::

            Document this method!!!
        """
        print >> sys.stdout, objectiveValue,
        if len(constraintValues) > 0:
            for i in range(len(constraintValues)):
                print >> sys.stdout, constraintValues[i],
            print ""
        return

    def generate_surrogate(self):
        """
        .. warning::

            Document this method!!!
        """
        return

    def generate_executable_file(self):
        """
        Generate Python code to play the role of black box executable.
        """

        tab = ' '*4
        endl = '\n'
        comment = '# '
        bb = open(self.file_name, 'w')
        # Import the neccessary modules
        bb.write('import os' + endl)
        bb.write('import sys' + endl)
        bb.write('import string' + endl)
        bb.write('import shutil' + endl)
        bb.write('import pickle' + endl)
        bb.write('import logging' + endl)
        bb.write('from opal.Solvers.nomad import NOMADBlackbox' + endl)
        
        bb.write(comment + 'Create an evaluator (model evaluation environment' + \
                     endl)
        bb.write('env = NOMADBlackbox()' + endl)
        bb.write('env.load(file="env.conf")' + endl)
        bb.write(comment + 'Activate the environment' + endl)
        bb.write('env.start()')
        bb.write(comment + 'Creeate a message that request to model values' + \ 
                 endl)
        bb.write(comment + 'The content of message is values read from a ' + \ 
                 'input file' + endl) 
        bb.write('msg = Message()' + endl)
        bb.write(comment + 'Raise an event by created message' + endl)
        bb.write('env.send_message(message=msg)' + endl)
        bb.write(comment + 'Wait for environement finish his life time' + endl)
        bb.write('env.join()' + endl)
        bb.write('env.dump(file="env.conf"' + endl)
        bb.close()
        return

    def run(self):
        inputValues = []
        paramValues = []
        #print args
        (inputValues, paramValues) = self.read_input(*args, **kwargs)
        if self.model is None:
            return
        #print inputValues
        (objective,constraints) = self.model.evaluate(inputValues)
        self.write_output(objective,constraints)
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

#   def blackbox_read_input(self,argv):
#        inputValues = [] # blackbox input = algorithm parameter
#        paramValues = [] # blackbox parameter
#        if len(argv) < 1:
#            return (inputValues,paramValues)
#        f = open(argv[1])
#        map(lambda l: inputValues.extend(l.strip('\n').strip(' ').split(' ')), f.readlines()) # Extract every words from the file and save to a list
#        f.close()
#        return (inputValues,paramValues)

#    def blackbox_write_output(self,objectiveValue,constraintValues):
#        print >> sys.stdout, objectiveValue,
#        if len(constraintValues) > 0:
#            for i in range(len(constraintValues)):
#                print >> sys.stdout,constraintValues[i],
#            print ""
#        return

    def solve(self, model=None, surrogate=None):
        self.blackbox = NOMADBlackbox(model=model)
        self.blackbox.generate_executable_file()
        if surrogate is not None:
            self.surrogate = NOMADBlackbox(model=surrogate)
            self.surrogate.generate_executable_file()
        #   surrogate.save()
        self.initialize()
        self.run()
        return

    def initialize(self):
        "Write NOMAD config to file based on parameter optimization problem."

        descrFile = open(self.paramFileName, "w")

        if self.blackbox.model is not None:
            model = self.blackbox.model
            descrFile.write('DIMENSION ' + str(model.n_var) + '\n')
            # descrFile.write('DISPLAY_DEGREE 4\n')
            descrFile.write('DISPLAY_STATS EVAL BBE [ SOL, ] OBJ TIME \\\\\n')
            descrFile.write('BB_EXE "$python ' + \
                    self.blackbox.file_name + '"\n')
            bbTypeStr = 'BB_OUTPUT_TYPE OBJ'
            for i in range(model.m_con):
                bbTypeStr = bbTypeStr + ' PB'
            descrFile.write(bbTypeStr + '\n')
            #surrogate = self.surrogate
            if self.surrogate is not None:
                descrFile.write('SGTE_EXE "$python ' + \
                                    self.surrogate.file_name + '"\n')
            pointStr = str(model.initial_points)
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
                '$EVAL$ & $BBE$ & $BBO$ & [ $SOL$ ] & $OBJ$ & $TIME$ \\\\\n')
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
        self.mpi_config['np'] = None # If set this to None, the number process is
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

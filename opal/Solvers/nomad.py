import sys
import os
import logging
from ..core.solver import Solver
from ..core.set import Set
#from ..core.blackbox import BlackBox

__docformat__ = 'restructuredtext'

class NOMADSpecification:
    "Used to specify black-box solver options."

    def __init__(self,name=None,value=None,**kwargs):
        self.name = name
        self.value = value
        pass

    def identify(self):
        return self.name

    def str(self):
        if (self.name is not None) and (self.value is not None):
            return self.name + ' ' + str(self.value)
        return ""

class NOMADBlackbox:
    """

    NOMADBlackbox contains
    the description and the method of communication between
    NOMAD solver and an executable blackbox.

    In other words, NOMAD blackbox is a wrapper that cover
    the model evaluator of a problem. An executable of wrapper is
    created to communicate with NOMAD. In this executable, the I/O
    stubs obey NOMAD's IO rule: input is a file, output to screen.

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

    def read_input(self, *args, **kwargs):
        """
        .. warning::

            Document this method!!!
        """
        inputValues = []
        paramValues = []
        #print args
        #print ""
        if len(args) < 1:
            return (inputValues, paramValues)

        # Extract every words from the file and save to a list
        f = open(args[1])
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
        bb = open(self.file_name, 'w')
        # To avoid the error compability of python version (local version
        # intalled by user) and global version (system), we don't make black
        # box an executable but call it via `python blackbox.py`
        # --------
        # or predifine config.python to the used python
        # rootPackage = config.__name__.replace('.config','')
        #bb.write(config.python + '\n')
        bb.write('#!/usr/bin/env python\n')
        bb.write('import os\n')
        bb.write('import sys\n')
        bb.write('import string\n')
        bb.write('import shutil\n')
        bb.write('import pickle\n')
        bb.write('import logging\n')
        bb.write('from opal.Solvers.nomad import NOMADBlackbox\n')
        bb.write('# Load test data.\n')
        bb.write('try:\n')
        bb.write(tab + 'blackboxDataFile = open("' + \
                self.model.data_file + '","r")\n')
        bb.write(tab + 'blackboxModel = pickle.load(blackboxDataFile)\n')
        bb.write(tab+'blackboxDataFile.close()\n')
        bb.write('except TypeError:\n')
        bb.write(tab+'print "Error in loading"\n')
        bb.write('blackbox = NOMADBlackbox(model=blackboxModel)\n')
        bb.write('blackbox.run(*sys.argv)\n')
        bb.write('blackboxModel.save()\n')
        bb.close()
        return

    def run(self, *args, **kwargs):
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
        self.result_file = None
        self.solution_file = None
        self.blackbox = None
        self.surrogate = None
        # List of line in parameter file
        self.parameter_settings = Set(name='NOMAD specification')

        return

    def solve(self, blackbox=None, surrogate=None):
        if isinstance(blackbox, NOMADBlackbox):
            self.blackbox = blackbox
        else:
            self.blackbox = NOMADBlackbox(model=blackbox)
        self.blackbox.generate_executable_file()
        if surrogate is not None:
            if isinstance(surrogate, NOMADBlackbox):
                self.surrogate = surrogate
            else:
                self.surrogate = NOMADBlackbox(model=surrogate,
                                               fileName='surrogate.py')
            self.surrogate.generate_executable_file()
        #   surrogate.save()
        self.initialize()
        self.run()
        self.finalize()
        return

    def initialize(self):
        "Write NOMAD config to file based on parameter optimization problem."

        if self.blackbox is None:
            return

        model = self.blackbox.model

        self.set_parameter(name='DIMENSION', value=str(model.n_var))
        self.set_parameter(name='DISPLAY_DEGREE', value=1)
        self.set_parameter(name='DISPLAY_STATS',
                           value='EVAL BBE [ SOL, ] OBJ TIME')
        self.set_parameter(name='BB_EXE',
                           value='"$python ' +  self.blackbox.file_name + '"')

        bbInputType = '( '
        for p in model.variables:
            if p.is_real:
                bbInputType += 'R '
            elif p.is_integer:
                bbInputType += 'I '
            elif p.is_binary:
                bbInputType += 'B '
            elif p.is_categorical:
                bbInputType += 'C '
            else:
                msg = 'Unrecognized parameter kind for %s' % p.name
                raise ValueError, msg
        bbInputType += ')'
        self.set_parameter(name='BB_INPUT_TYPE', value=bbInputType)

        bbTypeStr = 'OBJ'
        for i in range(model.m_con):
            bbTypeStr = bbTypeStr + ' PB'
        self.set_parameter(name='BB_OUTPUT_TYPE',
                           value=bbTypeStr)

        if self.surrogate is not None:
            self.set_parameter(name='SGTE_EXE',
                               value='"$python ' + \
                               self.surrogate.file_name + '"')

        pointStr = str(model.initial_point)
        self.set_parameter(name='X0',
                           value= pointStr.replace(',',' '))

        if model.bounds is not None:
            lowerBoundStr = str([bound[0] for bound in model.bounds \
                                     if bound is not None])\
                                     .replace('None','-').replace(',',' ')
            upperBoundStr = str([bound[1] for bound in model.bounds \
                                     if bound is not None])\
                                     .replace('None','-').replace(',',' ')
            if len(lowerBoundStr.replace(']','').replace('[','')) > 1:
                self.set_parameter(name='LOWER_BOUND',
                                   value=lowerBoundStr)
            if len(upperBoundStr.replace(']','').replace('[','')) > 1:
                self.set_parameter(name='UPPER_BOUND',
                                   value=upperBoundStr)
        # Write other settings.

        if self.solution_file is not None:
            self.set_parameter(name='SOLUTION_FILE',
                               value=self.solution_file)
        if self.result_file is not None:
            self.set_parameter(name='STATS_FILE',
                               value=self.result_file + \
                               ' EVAL & BBE & [ SOL ] & OBJ & TIME \\\\')

        descrFile = open(self.paramFileName, "w")
        for param_setting in self.parameter_settings:
            descrFile.write(param_setting.str() + '\n')
        descrFile.close()

        return

    def set_parameter(self, name=None, value=None):
        param = NOMADSpecification(name=name,value=value)
        self.parameter_settings.append(param)
        return

    def run(self):
        os.system('nomad ' + self.paramFileName)
        return

    def finalize(self):
        # Clean up the temporary file
        if os.path.exists('blackbox.py'):
            os.remove('blackbox.py')

        if os.path.exists('blackbox.dat'):
            os.remove('blackbox.dat')

        if os.path.exists('surrogate.py'):
            os.remove('surrogate.py')

        if os.path.exists('surrogate.dat'):
            os.remove('surrogate.dat')

        if os.path.exists(self.paramFileName):
            os.remove(self.paramFileName)
        return

class NOMADMPISolver(NOMADSolver):
    def __init__(self,
                 name='NOMAD.MPI',
                 parameterFile='nomad.mpi-param.txt',
                 np=None,
                 **kwargs):
        NOMADSolver.__init__(self, name=name, parameterFile=parameterFile)
        self.mpi_config = {}  # Contains the settings for MPI environment
        self.mpi_config['np'] = None  # If set this to None, the number process is
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

import sys
import os
from ..core.solver import Solver
from ..core.blackbox import BlackBox

class Parameter:
    def __init__(self,name=None,value=None,**kwargs):
        self.name = name
        self.value = value
        pass
    
    def str(self):
        if (self.name is not None) and (self.value is not None):
            return self.name + ' ' + str(self.value)
        return ""
    
class NOMADBlackbox(BlackBox):
    '''
    NOMADBlackbox is an implementation of BlackBox, it contains
    the description and the method of communication between 
    NOMAD solver and an executable blackbox.
    The descriptions include the executable file name
    The communicating methods are read_input and write_output
    Those are specialized to NOMAD solver
    '''
    def __init__(self,solver=None,model=None,fileName='blackbox.py',**kwargs):
        BlackBox.__init__(self,solver=solver,model=model,**kwargs)
        self.file_name = fileName
        self.surrogate = None
        pass
     
    def read_input(self,*args,**kwargs):
        inputValues = []
        paramValues = []
        if len(argv) < 1:
            return (inputValues,paramValues)
        f = open(args[1])
        map(lambda l: inputValues.extend(l.strip('\n').strip(' ').split(' ')), f.readlines()) # Extract every words from the file and save to a list
        f.close()
        return (inputValues,paramValues)
    
    def write_output(self,objectiveValue,constraintValues):
        print >> sys.stdout, objectiveValue,
        if len(constraintValues) > 0:
            for i in range(len(constraintValues)):
                print >> sys.stdout,constraintValues[i],
            print ""
        return
   
    def generate_surrogate(self):
        return

    def generate_executable_file(self):
        
        tab = ' '*4
        blackboxFile = open(self.file_name,'w')
        # To avoid the error compability of python version (local version intalled by user) and
        # global version (system), we don't turn black box as a executable but call it by
        # python blackbox.py
        # --------
        # or predifine config.python to the used python
        # rootPackage = config.__name__.replace('.config','')
        #blackboxFile.write(config.python + '\n')
        #blackboxFile.write('#!/usr/bin/env python\n')
        blackboxFile.write('import os\n')
        blackboxFile.write('import sys\n')
        blackboxFile.write('import string\n')
        blackboxFile.write('import shutil\n')
        blackboxFile.write('import pickle\n')
        #blackboxFile.write('from ' + rootPackage + '.core import modeldata\n')
        #blackboxFile.write('from ' + rootPackage + '.core import blackbox\n')
        #if self.solver is not None:
        #    blackboxFile.write('from ' + rootPackage + '.Solvers import ' + self.solver.name + '\n')
        #blackboxFile.write('from ' + self.modelEvaluator.model.moduleName + ' import '+ self.modelEvaluator.model.objFuncName + '\n')
        #for constraint in self.modelEvaluator.model.constraintNames:
        #    blackboxFile.write('from ' + self.modelEvaluator.model.moduleName + ' import '+ constraint + '\n')
        blackboxFile.write('# load the test data\n')
        blackboxFile.write('try:\n')
        blackboxFile.write(tab+'blackboxDataFile = open("' + self.model.data_file + '","r")\n')
        blackboxFile.write(tab+'blackboxModel = pickle.load(blackboxDataFile)\n')
        blackboxFile.write(tab+'blackboxDataFile.close()\n')
        blackboxFile.write('except TypeError:\n')
        blackboxFile.write(tab+'print "Error in loading"\n')
        blackboxFile.write('blackbox = NOMADBlackBox(model=blackboxModel)\n')
        #blackboxFile.write('blackbox.opt_data.synchronize_measures()\n')
        blackboxFile.write('blackbox.run(sys.argv)\n')
        #blackboxFile.write('try:\n')
        #blackboxFile.write(tab+'blackboxDataFile = open("' + self.dataFileName + '","w")\n')
        #blackboxFile.write(tab+'pickle.dump(blackbox,blackboxDataFile)\n')
        #blackboxFile.write(tab+'blackboxDataFile.close()\n')
        #blackboxFile.write('except TypeError:\n')
        #blackboxFile.write(tab+'print "Error in loading"\n')
        blackboxFile.write('blackbox.save()\n')
        #blackboxFile.write('blackboxRunLogFile.close()\n')
        blackboxFile.close()
        #os.chmod(self.runFileName,0755)
        return
    
class NOMADSolver(Solver):
    """
    An implemtation of Solver abstract class. 
    An object of NOMADSolver represent for the NOMAD solver
    For more information about the NOMAD, go to
    http://wwww.gerad.ca/NOMAD
    """
    def __init__(self,**kwargs):
        Solver.__init__(self,name='NOMAD',command='nomad',parameter='nomad-param.txt',**kwargs)
        self.paramFileName = 'nomad-param.txt'
        self.resultFileName = 'nomad-result.txt'
        self.solutionFileName = 'nomad-solution.txt'
        self.blackbox = NOMADBlackbox(solver=self)
        self.parameter_settings = [] # List of line in parameter file
        pass

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
    
    def solve(self,model=None,surrogate=None):
        self.blackbox.model = model
        self.blackbox.generate_executable_file()
        if surrogate is not None:
            surrogate.generate_executable_file()
#            surrogate.save()
        self.initialize()
        self.run()
        return

    def initialize(self):
        descriptionFile = open(self.paramFileName,"w")
        # Create problem descriptions basing on
        # the model of blackbox
        if self.blackbox.model is not None:
            model = self.blackbox.model
            descriptionFile.write('DIMENSION ' + str(model.n_var) + '\n')
            # descriptionFile.write('DISPLAY_DEGREE 4\n')
            descriptionFile.write('DISPLAY_STATS EVAL& BBE & SOL&  &OBJ \\\\ \n')
            descriptionFile.write('BB_EXE "$python ' + self.blackbox.file_name + '"\n')
            # descriptionFile.write('BB_EXE ' + blackbox.executableFileName + '\n')
            bbTypeStr = 'BB_OUTPUT_TYPE OBJ'
            for i in range(model.m_con):
                bbTypeStr = bbTypeStr + ' PB'
            descriptionFile.write(bbTypeStr + '\n')
            surrogate = self.blackbox.surrogate
            if surrogate is not None:
                descriptionFile.write('SGTE_EXE "$python ' + surrogate.file_name + '"\n')
            pointStr = str(model.initial_points)
            descriptionFile.write('X0 ' +  pointStr.replace(',',' ') + '\n')
            #print 'NOMAD.py',[bound[0] for bound in blackbox.bounds]
            lowerBoundStr = str([bound[0] for bound in model.bounds]).replace('None','-').replace(',',' ')
            upperBoundStr = str([bound[1] for bound in model.bounds]).replace('None','-').replace(',',' ')
            descriptionFile.write('LOWER_BOUND ' + lowerBoundStr + '\n')
            descriptionFile.write('UPPER_BOUND ' + upperBoundStr + '\n')
        # Write the other settings
        descriptionFile.write('SOLUTION_FILE ' + self.solutionFileName + '\n')
        descriptionFile.write('STATS_FILE ' + self.resultFileName + ' EVAL& BBE & BBO & SOL&  &OBJ \\\\ \n')
        for param_setting in self.parameter_settings:
            descriptionFile.write(param_setting + '\n')
        descriptionFile.close()
        return

    def set_parameter(self,name=None,value=None):
        #descriptionFile = open(self.paramFileName,'a')
        #descriptionFile.write(param.str() + '\n')
        #descriptionFile.close()
        param = Parameter(name=name,value=value)
        self.parameter_settings.append(param.str())
        return

    def run(self):
        return
NOMAD = NOMADSolver()

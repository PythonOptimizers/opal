import os
import sys
import os.path
import pickle

from .. import config
from .modelstructure import ModelEvaluator

class BlackBox:
    def __init__(self, modelData=None, modelStructure=None,
                 runFileName='blackbox.py',dataFileName='blackbox.dat',logFileName='test.log',**kwargs):
        """
        This class represent a black box that encapsulates the 
        information of a parameter optimization problem.
        From the parameter problem point of view, this class contains
        two descriptions: model data and model struture
        From the black box point of view, this class represents for 
        an executable file whose I/O methods depend from the specific solver.
        To create an BlackBox object, users have to specify two mains 
        component
        blackbox = BlackBox(modelStructure,modelData)
        """

        self.model_data = modelData
        self.model_structure = modelStructure
        self.runFileName = runFileName
        self.dataFileName = dataFileName
        self.logFileName = logFileName
        activeParameters = self.model_data.get_active_parameters()
        self.n_var = len(activeParameters)
        self.m_con = len(self.model_structure.constraints)
        self.initial_points = [param.value for param in activeParameters]
        self.bounds = [param.bound for param in activeParameters]
        self.solver = None 
        # if no solver is specified, the blackbox is a general 
        # executable file with two arguments: input file and parameter file
        # The output is standard screen
        pass

    def set_options(self,**kwargs):
        return
    
    def generate_executable_file(self):
        
        tab = ' '*4
        blackboxFile = open(self.runFileName,'w')
        # To avoid the error compability of python version (local version intalled by user) and
        # global version (system), we don't turn black box as a executable but call it by
        # python blackbox.py
        # --------
        # or predifine config.python to the used python
        rootPackage = config.__name__.replace('.config','')
        #blackboxFile.write(config.python + '\n')
        #blackboxFile.write('#!/usr/bin/env python\n')
        blackboxFile.write('import os\n')
        blackboxFile.write('import sys\n')
        blackboxFile.write('import string\n')
        blackboxFile.write('import shutil\n')
        blackboxFile.write('import pickle\n')
        blackboxFile.write('from ' + rootPackage + '.core import modeldata\n')
        blackboxFile.write('from ' + rootPackage + '.core import blackbox\n')
        if self.solver is not None:
            blackboxFile.write('from ' + rootPackage + '.Solvers import ' + self.solver.name + '\n')
        #blackboxFile.write('from ' + self.modelEvaluator.model.moduleName + ' import '+ self.modelEvaluator.model.objFuncName + '\n')
        #for constraint in self.modelEvaluator.model.constraintNames:
        #    blackboxFile.write('from ' + self.modelEvaluator.model.moduleName + ' import '+ constraint + '\n')
        blackboxFile.write('# load the test data\n')
        blackboxFile.write('try:\n')
        blackboxFile.write(tab+'blackboxDataFile = open("' + self.dataFileName + '","r")\n')
        blackboxFile.write(tab+'blackbox = pickle.load(blackboxDataFile)\n')
        blackboxFile.write(tab+'blackboxDataFile.close()\n')
        blackboxFile.write('except TypeError:\n')
        blackboxFile.write(tab+'print "Error in loading"\n')
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

    def run(self,argv):
        '''

        This method for all possible things in blackbox.py
        Pay attention to the imports,
        output = run(input)
        
        '''
        inputValues = [] # algorithm parameter values
        paramValues = [] # blackbox parameter values
        # Get the parameter values from the input of blackbox
        if self.solver is not None:
            (inputValues,paramValues) = self.solver.blackbox_read_input(argv)
        else:
            (inputValues,paramValues) = self.read_input(argv)
        #print '[blackbox.py] ', paramValues
        self.model_data.run(inputValues)
        
        testResult = self.model_data.get_test_result()
        #print 'ho ho after getTestResult', self.modelData.measures[0],\
         #      self.modelData.measures[0].valuetable
        modelEvaluator = ModelEvaluator(self.model_structure,self.model_data.measures)
        (funcObj,constraints) = modelEvaluator.evaluate(testResult)
        if self.solver is not None:
            self.solver.blackbox_write_output(funcObj,constraints)
        else:
            self.write_output(funcObj,constraints)
        self.log()
        return
    
    def read_input(self,argv):
        inputValues = []
        paramValues = []
        if len(argv) < 1:
            return (inputValues,paramValues)
        f = open(argv[1])
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

    def solve(self,solver):
        self.solver = solver
        self.generate_executable_file()
        self.save()
        self.solver.initialize(self)
        self.solver.run()
        return
    
    def save(self):
        try:
            blackboxDataFile = open(self.dataFileName,"w")
            pickle.dump(self,blackboxDataFile)
            blackboxDataFile.close()
        except TypeError:
            print "Error in saving"
        return
    
    def log(self):
        if self.model_data.log != None:
            self.model_data.log(self.logFileName)
        if self.model_structure.log != None:
            self.model_structure.log(self.logFileName)
        return



import os
import os.path
import pickle

from .. import config
from .modelstructure import ModelEvaluator


class BlackBox:
    def __init__(self, optModel=None, optData=None,
                 fileName=None,**kwargs):

        self.opt_data = optData
        self.opt_model = optModel
        if fileName is None:
            self.executableFileName = 'blackbox.py'
        else:
            self.executableFileName = fileName
        self.nVar = len(optData.activeParameters)
        self.mCon = len(optModel.constraints)
        self.initialPoint = [param.value for param in optData.activeParameters]
        pass

    def set_options(self,**kwargs):        
        return
    
    def generate_executable_file(self):
        
        blackboxFile = open(self.executableFileName,'w')
        # To avoid the error compability of python version (local version intalled by user) and
        # global version (system), we don't turn black box as a executable but call it by
        # python blackbox.py
        # --------
        # or predifine config.python to the used python
        rootPackage = config.__name__.replace('.config','')
        blackboxFile.write(config.python + '\n')
        #Blackboxfile.write('#!python\n')
        blackboxFile.write('import os\n')
        blackboxFile.write('import sys\n')
        blackboxFile.write('import string\n')
        blackboxFile.write('import shutil\n')
        blackboxFile.write('import pickle\n')
        blackboxFile.write('from ' + rootPackage + '.core import modeldata\n')
        blackboxFile.write('from ' + rootPackage + '.core import blackbox\n')
        blackboxFile.write('from ' + rootPackage + '.Solvers import ' + self.solver.name + '\n')
        blackboxFile.write('from ' + rootPackage + '.Measures import * \n')
        #blackboxFile.write('from ' + os.path.basename(self.opt_model.objective.file_name).strip('.py') + ' import ' + self.opt_model.objective.name + '\n')
        #blackboxFile.write('from ' + self.modelEvaluator.model.moduleName + ' import '+ self.modelEvaluator.model.objFuncName + '\n')
        #for constraint in self.modelEvaluator.model.constraintNames:
        #    blackboxFile.write('from ' + self.modelEvaluator.model.moduleName + ' import '+ constraint + '\n')
        blackboxFile.write('# load the test data\n')
        blackboxFile.write('try:\n')
        blackboxFile.write('\t blackboxDataFile = open("blackbox.dat","r")\n')
        blackboxFile.write('\t blackbox = pickle.load(blackboxDataFile)\n')
        blackboxFile.write('\t blackboxDataFile.close()\n')
        blackboxFile.write('except TypeError:\n')
        blackboxFile.write('\t print "Error in loading"\n')
        blackboxFile.write('blackbox.opt_data.synchronize_measures()\n')
        blackboxFile.write('blackbox.run(sys.argv)\n')
        blackboxFile.write('try:\n')
        blackboxFile.write('\t blackboxDataFile = open("blackbox.dat","w")\n')
        blackboxFile.write('\t pickle.dump(blackbox,blackboxDataFile)\n')
        blackboxFile.write('\t blackboxDataFile.close()\n')
        blackboxFile.write('except TypeError:\n')
        blackboxFile.write('\t print "Error in loading"\n')
        #blackboxFile.write('blackboxRunLogFile.close()\n')
        blackboxFile.close()
        os.chmod(self.executableFileName,0755)
        return

    def run(self,argv):
        '''

        This method for all possible things in blackbox.py
        Pay attention to the imports,
        output = run(input)
        
        '''
        paramValues = []
        # Get the parameter values from the input of blackbox

        paramValues = self.solver.read_input(argv)
        self.opt_data.run(paramValues)
        
        testResult = self.opt_data.get_test_result()
        #print 'ho ho after getTestResult', self.optData.measures[0],\
         #      self.optData.measures[0].valuetable
        modelEvaluator = ModelEvaluator(self.opt_model,self.opt_data.measures)
        (funcObj,constraints) = modelEvaluator.evaluate(testResult)
        self.solver.write_output(funcObj,constraints)
        self.log('test.log')
        return
    
    def solve(self,solver):
        self.solver = solver
        self.generate_executable_file()
        self.save()
        self.solver.initialize(self)
        self.solver.run()
        return
    
    def save(self,fileName='blackbox.dat'):
        try:
            blackboxDataFile = open(fileName,"w")
            pickle.dump(self,blackboxDataFile)
            blackboxDataFile.close()
        except TypeError:
            print "Error in loading"
        return
    
    def log(self,fileName='blackbox.log'):
        if self.opt_data.log != None:
            self.opt_data.log(fileName)
        if self.opt_model.log != None:
            self.opt_model.log(fileName)
        return



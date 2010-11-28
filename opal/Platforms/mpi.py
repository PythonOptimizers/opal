
import os
import time

from ..core.platform import Platform

class MPIPlatform(Platform):
    def __init__(self,**kwargs):
        Platform.__init__(self,'MPI',**kwargs)
        #self.communicator = MPI.COMM_WORLD
        self.children = []
        self.wrapper_name = 'run_wrapper_'
        self.configuration = {}
        pass
   
    def set_config(self, parameterName, parameterValue):
        self.configuration[parameterName] = parameterValue 
        return

    def initialize(self, testId):
        self.wrapper_name = self.wrapper_name + testId + '.py'
        if not os.path.exists(self.wrapper_name):
            self.create_wrapper()            
        self.children = []
        return

    def execute(self, command, output='/dev/null'):
        jobId = str(hash(command))
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + self.configuration[param] + " "
        #child = self.communicator.Spawn('python',
        #                        [self.wrapper_name, command])
        from mpi4py import MPI
        child = MPI.COMM_WORLD.Spawn('python',
                                     [self.wrapper_name, command])
        self.children.append(child)
        return 

    def create_wrapper(self):
        tab = ' '*4
        f = open(self.wrapper_name,'w')
        f.write('import sys\n')
        f.write('import os\n')
        f.write('from mpi4py import MPI\n')
        f.write('parent = MPI.COMM_WORLD.Get_parent()\n')
        f.write('exeCmd = ""\n')
        f.write('for argv in sys.argv[1:]:\n')
        f.write(tab + 'exeCmd = exeCmd + argv + " "\n')
        #f.write('print exeCmd\n')
        f.write('os.system(exeCmd)\n')
        f.write('parent.Barrier()\n')
        f.write('parent.Disconnect()\n')
        f.close()
        
        
    def waitForCondition(self,condition):
        for child in self.children:
            child.Barrier()
            child.Disconnect()
        os.remove(self.wrapper_name)
        self.children = []
        return
    

OPALMPI = MPIPlatform()

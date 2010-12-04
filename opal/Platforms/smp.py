
import os
import time
import subprocess

from ..core.platform import Platform
from ..core import log

class SMPPlatform(Platform):
    def __init__(self,logHandlers=[],**kwargs):
        Platform.__init__(self,'SMP',**kwargs)
        self.children = []
        self.configuration = {}
        self.logger = log.OPALLogger(name='smpPlatform', handlers=logHandlers)
        pass
   
    def set_config(self, parameterName, parameterValue):
        self.configuration[parameterName] = parameterValue 
        return

    def initialize(self, testId):      
        self.children = []
        self.logger.log('Platform is initialized for the test ' + testId)
        return

    def execute(self, command, output='/dev/null'):
        jobId = str(hash(command))
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + \
                self.configuration[param] + " " 
        cmd = command.split(' ')
        child = subprocess.Popen(args=cmd)
        self.logger.log(command + \
                            ' is executed with id ' + str(child.pid)) 
        self.children.append(child)
        return 
        
    def waitForCondition(self,condition):
        for child in self.children:
            if child.poll() is None:
                child.wait()
            self.logger.log(str(child) + ' with id ' +
                            str(child.pid) + ' finish his work')
            del child
        self.children = []
        return
    

SMP = SMPPlatform()

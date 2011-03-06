
import os
import time
import subprocess
import threading

from ..core.platform import Platform
from ..core.platform import Task

from ..core import log


class SMPTask(Task):
    """
    
    Each task run on this platform need to
    some stubs to communicate with the platform
    
    """
    def __init__(self, id=None, command=None):
        Task.__init__(self, id=id, command=command)
        self.proc = None
        self.pid = None
        return

    def run(self):
        cmd = self.command.split(' ')
        self.proc = subprocess.Popen(args=cmd)
        self.pid = proc.pid
        if self.proc.poll() is None: # check if child process is still running
            self.proc.wait() # wait until the child process finish
        # Inform the task is finished
        msg = Message()
        self.send_message(msg)
        return

class SMPPlatform(Platform):
    def __init__(self,logHandlers=[],**kwargs):
        Platform.__init__(self,'SMP',**kwargs)
        #self.task_monitor = threading.Thread()
        #self.children = []
        self.configuration = {}
        self.logger = log.OPALLogger(name='smpPlatform', handlers=logHandlers)
        pass
   
    def set_config(self, parameterName, parameterValue):
        self.configuration[parameterName] = parameterValue 
        return

    def initialize(self, testId):      
        #self.children = []
        self.logger.log('Platform is initialized for the test ' + testId)
        return

    def create_task(self, command, output='/dev/null'):
        jobId = str(hash(command))
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + \
                self.configuration[param] + " "
        cmdStr = optionStr + command
        task = SMPTask(command=cmdStr)
        return 
    
    def finalize(self, testId=None):
        while (self.get_running_tasks() > 0):
            pass
        return
        
  

SMP = SMPPlatform()


import os
import time
import subprocess
import threading
import shlex

from ..core.platform import Platform
from ..core.platform import Task

from ..core import log


class SMPTask(Task):
    """
    
    Each task run on this platform need to
    some stubs to communicate with the platform
    
    """
    def __init__(self, name=None, taskId=None, command=None):
        Task.__init__(self, name=name, taskId=taskId, command=command)
        self.proc = None
        self.pid = None
        return

    def run(self):
        cmd = shlex.split(self.command)
        self.proc = subprocess.Popen(args=cmd)
        self.pid = self.proc.pid
        if self.proc.poll() is None: # check if child process is still running
            self.proc.wait() # wait until the child process finish
        # Inform the task is finished
        Task.run(self)
        return

class SMPPlatform(Platform):
    def __init__(self, maxTask=2, logHandlers=[]):
        Platform.__init__(self, name='SMP',
                          maxTask=2,
                          synchronous=False,
                          logHandlers=logHandlers)
        self.configuration = {}
        #self.logger = log.OPALLogger(name='smpPlatform', handlers=logHandlers)
        self.message_handlers['cfp-execute'] = self.create_task
        pass
   
    def set_config(self, parameterName, parameterValue):
        self.configuration[parameterName] = parameterValue 
        return

    def initialize(self, testId):      
        #self.children = []
        #self.logger.log('Platform is initialized for the test ' + testId)
        return

    # Message handlers
    
    def create_task(self, info):
        '''

        Handle a call for proposal of executing a command
        '''
        if 'proposition' not in info.keys():
            self.logger.log('Proposal of executing a command has not ' + \
                            'information to prcess')
            return

        proposition = info['proposition']
        command = proposition['command']
        if 'output' in proposition.keys():
            output = proposition['output']
        else:
            output='/dev/null'
        name = proposition['tag']
        if 'queue' in proposition.keys():
            queueTag = proposition['queue']
        else:
            queueTag = None
        jobId = str(hash(command))
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + \
                self.configuration[param] + " "
        cmdStr = optionStr + command
        task = SMPTask(name=name,
                       command=cmdStr)
        self.submit(task, queue=queueTag)
        return 
  
        
  

SMP = SMPPlatform()

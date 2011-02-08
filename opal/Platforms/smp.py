
import os
import time
import subprocess
import threading

from ..core.platform import Platform
from ..core import log


class TaskWrapper(threading.Thread):
    """
    
    Each task run on this platform need to
    some stubs to communicate with the platform
    
    """
    def __init__(self, platform=None, command=None):
        self.command = command
        self.proc = None
        self.pid = None
        self.platform=platform
        return

    def run(self):
        cmd = self.command.split(' ')
        self.proc = subprocess.Popen(args=cmd)
        self.pid = proc.pid
        if self.proc.poll() is None: # check if child process is still running
            self.proc.wait() # wait until the child process finish
        # Inform the task is finished
        event = Message(type='Event',
                        source='Platform',
                        destination=None,
                        content=command + ' is finished')
        self.platform.push(event)
        
        return

class SMPPlatform(Platform):
    def __init__(self,logHandlers=[],**kwargs):
        Platform.__init__(self,'SMP',**kwargs)
        #self.task_monitor = threading.Thread()
        #self.children = []
        self.tasks = []
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

    def submit(self, command, output='/dev/null'):
        jobId = str(hash(command))
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + \
                self.configuration[param] + " "
 
        #cmd = command.split(' ')
        #child = subprocess.Popen(args=cmd)
        task = TaskWrapper(command=command)
        task.start()
        self.logger.log(command + \
                            ' is executed with id ' + str(task.pid))
        self.tasks.append(task)
        # Inform to the task monitor that 
        # a task is submitted.
        event = TaskEvent(command=command, status='Submitted')
        self.push(event)
        return 
    
    def finalize(self, testId=None):
        while (self.get_running_tasks() > 0):
            pass
        return
        
    def get_running_tasks(self):
        i = 0
        while i < len(self.tasks):
            if self.tasks[i].proc.poll() is not None: # The child process is terminated
                del self.tasks[i]    # if an element of list is removed, the index 
                                              # does not need update
            else:
                i++                           # Update index
        return len(self.tasks)
       
    def terminate(self):
        while len(self.task_processes) > 0:
            if self.tasks[i].proc[i].poll() is None: # The child process is not terminated
                self.tasks[i].proc.kill()
                self.tasks.stop()
            del self.tasks[i]
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

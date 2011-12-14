import socket
import os
import time

from ..core.platform import Platform
from ..core.platform import Task

class LSFTask(Task):
    def __init__(self, name=None,
                 taskId=None,
                 command=None,
                 lsfOptions=None,
                 logHandlers=[]):
        self.output = "-N -oo /tmp/lsf-output.log" 
        lsfCmd = "bsub " + \
                 "  -J " + taskId + optionStr + command
        Task.__init__(self,
                      name=name,
                      taskId=taskId,
                      command=lsfCmd,
                      logHandler=logHandlers)
        self.job_id = taskId
        return

    def run(self):
        os.system(self.command)
        os.wait('ended("' + self.job_id +')')
        Task.run(self)
        return

    def wait(self,condition):
        # This function playes in role of synchronyzers
        # 1 - Generate a synchronizing job including a segment code that
        #     notifies to current process by socket (notifyToMaster)
        # 2 - Prepare a waiting socket: create, bind, ..
        # 3 - Submit the synchronizing with the condition specified in
        #     the condition
        # 4 - Turn in waiting by listening the notify at created socket
        # Argument condition may be "ended(CUTEr-*)"
        #-------------------
        # Set default socket parameter
        #-------------------
        port = 19879
        hostname = socket.gethostname()
        ltime = time.localtime()
        keyStr = str(ltime.tm_year) + str(ltime.tm_mon) +  str(ltime.tm_mday) +\
                 str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        #-------------------------
        # Prepare socket
        #-----------
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketIsBound = 0
        #-----------------
        # Choose an availble port to avoid conflit with the other routine
        # Particularly, the other parameter optimization
        while socketIsBound == 0:
            try:
                serversocket.bind((hostname, port))
                socketIsBound = 1
            except:
                port = port + 1
        #print "waiting at",socket.gethostname(), port
        serversocket.listen(1)
        #-----------------------
        #  Generating synchronizing job
        #----------------------
        synchronizerFile = 'synchronizer_' + self.job_id + '.py'
        f = open('synchronizer.py','w')
        #synchronizerFile.write('#!/usr/bin/env python\n')
        f.write('import socket\n')
        f.write('port = ' + str(port) + '\n')
        f.write('s = socket.socket(socket.AF_INET, ' + \
                'socket.SOCK_STREAM)\n')
        f.write('s.connect(("' + hostname + '",' + \
                str(port) + '))\n')
        f.write('s.send("'+ keyStr + '")\n')
        f.write('s.close()\n')
        f.close()
        
        #ltime = time.localtime()
        #timeStr = str(ltime.tm_year) + '-' + str(ltime.tm_mon) + '-' + \
        #          str(ltime.tm_mday) + ' ' + str(ltime.tm_hour) + ':' + \
        #          str(ltime.tm_min) + ':' + str(ltime.tm_sec)
        #os.system('echo ' + timeStr + ' Begin waiting >> lsf-sync.log')
        synchronizeCmd = 'bsub -w "' + condition + \
                         '" python ' + synchronizerFile + ' > /dev/null'
        os.system(synchronizeCmd)
        #-----------------------
        # Waiting for the notify from synchonizer
        # ---------------------
        recvKey = ''
        while recvKey != keyStr:
            (clientsocket, address) = serversocket.accept()
            recvKey = clientsocket.recv(len(keyStr))
            clientsocket.close()
        # print address, "is connected"
        #--------------
        # free the sockets if received a notification
        #-----------------

        #clientsocket.close()
        serversocket.close()
        #ltime = time.localtime()
        #timeStr = str(ltime.tm_year) + '-' + str(ltime.tm_mon) + '-' + \
        #          str(ltime.tm_mday) + ' ' + str(ltime.tm_hour) + ':' + \
        #          str(ltime.tm_min) + ':' + str(ltime.tm_sec)
        #os.system('echo ' + timeStr + ' End waiting >> lsf-sync.log')
        os.remove(synchronizerFile)
        return



class LSFPlatform(Platform):
    def __init__(self, maxTask=3, synchronous=False, logHandlers=[]):
        Platform.__init__(self,
                          name='LSF',
                          maxTask=maxTask,
                          logHandlers=logHandlers)
        self.configuration = {}
        self.message_handlers['cfp-execute'] = self.create_task
        pass

    def set_config(self, parameterName, parameterValue):
        self.configuration[parameterName] = parameterValue
        return

    def initialize(self, testId):
        return

    def create_task(self, info):
        '''

        Handle a call for proposal of executing a command through LSF platform
        '''

        if 'proposition' not in info.keys():
            self.logger.log('Proposal of executing a command has not ' + \
                            'information to process')
            return
        execCmd = info['proposition']['command']
        tag = info['proposition']['tag']
        if 'queue' in info['proposition'].keys():
            queueTag = info['proposition']['queue']
        else:
            queueTag = None
            
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + \
                        self.configuration[param] + " "
        if queueTag is not None:
            optionStr = " -g " + queueTag + optionStr
        task = LSFTask(name=tag,
                       taskId=tag,
                       command=execCmd,
                       lsfOptions=optionStr)
        self.submit(task, queue=queueTag)
        return 

LSF = LSFPlatform()

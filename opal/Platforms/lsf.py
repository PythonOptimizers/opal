import socket
import os
import time

from ..core.platform import Platform

class LSFPlatform(Platform):
    def __init__(self,submitLog='submit.log',**kwargs):
        Platform.__init__(self,'LSF',**kwargs)
        self.submitLog = submitLog
        self.configuration = {}
        self.group_id = None
        pass
   
    def set_config(self, parameterName, parameterValue):
        self.configuration[parameterName] = parameterValue 
        return

    def initialize(self, testId):
        self.group_id = "/g" + testId
        return

    def execute(self, command, output='/dev/null'):
        jobId = str(hash(command))
        # str(ltime.tm_year) +  str(ltime.tm_mon) + str(ltime.tm_mday) + \
            # str(ltime.tm_hour) + str(ltime.tm_min) + str(ltime.tm_sec)
        optionStr = " "
        for param in self.configuration.keys():
            optionStr = optionStr + param + " " + self.configuration[param] + " "
        os.system("bsub -N -oo " + output + " -g " + self.group_id + "  -J " + jobId + optionStr + command + " >> " + self.submitLog)
        return jobId


    def waitForCondition(self,condition):
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
        synchronizerFile = open('synchronizer.py','w')
        #synchronizerFile.write('#!/usr/bin/env python\n')
        synchronizerFile.write('import socket\n')
        synchronizerFile.write('port = ' + str(port) + '\n')
        synchronizerFile.write('s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n')
        synchronizerFile.write('s.connect(("' + hostname + '",' + str(port) + '))\n')
        synchronizerFile.write('s.send("'+ keyStr + '")\n')
        synchronizerFile.write('s.close()\n')
        synchronizerFile.close()
        #os.chmod('synchronizer.py',0755)
        #------------------------
        # Launch the synchronizer
        #------------------------
        ltime = time.localtime()
        timeStr = str(ltime.tm_year) + '-' + str(ltime.tm_mon) + '-' + str(ltime.tm_mday) + ' ' + \
                  str(ltime.tm_hour) + ':' + str(ltime.tm_min) + ':' + str(ltime.tm_sec)
        os.system('echo ' + timeStr + ' Begin waiting >> lsf-sync.log')
        synchronizeCmd = 'bsub -w "' + condition + '" python synchronizer.py >> lsf-sync.log'
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
        ltime = time.localtime()
        timeStr = str(ltime.tm_year) + '-' + str(ltime.tm_mon) + '-' + str(ltime.tm_mday) + ' ' + \
                  str(ltime.tm_hour) + ':' + str(ltime.tm_min) + ':' + str(ltime.tm_sec)
        os.system('echo ' + timeStr + ' End waiting >> lsf-sync.log')
        os.remove('synchronizer.py')
        return
    

LSF = LSFPlatform()

import socket
import os

from ..core.platform import Platform

class LINUXPlatform(Platform):
    def __init__(self,**kwargs):
        Platform.__init__(self,'LINUX',**kwargs)
        pass

    def initialize(self, testId):
        return

    def execute(self, command, output='/dev/null', commandId=None):
        '''
        
        This method will execute command and return process id in term 
        of his process management
        '''
        id = 'proc'
        os.system(command + ' > ' + output)
        return id

    def waitForCondition(self,condition):
        pass

LINUX = LINUXPlatform()

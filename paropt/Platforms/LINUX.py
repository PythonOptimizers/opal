import socket
import os

from ..core.platform import Platform

class LINUXPlatform(Platform):
    def __init__(self,**kwargs):
        Platform.__init__(self,'LINUX',**kwargs)
        pass

    def execute(self,command,output=None,commandId=None):
        if output is None:
            os.system(command + ' > output.log')
        else:
            os.system(command + ' > /dev/null')

    def waitForCondition(self,condition):
        pass

LINUX = LINUXPlatform()

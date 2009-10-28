import socket
import os

from ..core.platform import Platform

class LINUXPlatform(Platform):
    def __init__(self,**kwargs):
        Platform.__init__(self,'LINUX',**kwargs)
        pass

    def execute(self,command,output='/dev/null',commandId=None):
        os.system(command + ' > ' + output
)

    def waitForCondition(self,condition):
        pass

LINUX = LINUXPlatform()

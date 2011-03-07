import socket
import os

from ..core.platform import Platform
from ..core.platform import Task

class LINUXTask(Task):
    def __init__(self, command=None, output='/dev/null', logHandlers=[]):
        Task.__init__(self, command=command, output=output, logHandlers=logHandlers)
        return

    def run(self):
        os.system(self.command + ' > ' + self.output)


class LINUXPlatform(Platform):
    def __init__(self, logHandlers=[]):
        Platform.__init__(self, logHandlers=logHandlers)
        return

    def submit(self, command):
        '''
        
        This method will execute command and return process id in term 
        of his process management
        '''
        id = 'proc'
        task = LINUXTask(command=command)
        Platform.submit(self, task)
        return id

    def test_a(self):
        print 'Hello'

LINUX = LINUXPlatform()

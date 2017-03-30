import socket
import os

from ..core.platform import Platform
from ..core.platform import Task

class LINUXTask(Task):
    def __init__(self,
                 name=None,
                 command=None,
                 sessionTag=None,
                 output='/dev/null',
                 logHandlers=[]):
        Task.__init__(self,
                      name=name,
                      command=command,
                      sessionTag=sessionTag,
                      output=output,
                      logHandlers=logHandlers)
        return

    def run(self):
        # Execute the command
        os.system(self.command + ' > ' + self.output)
        # Inform the fininish
        Task.run(self)
        return

class LINUXPlatform(Platform):
    def __init__(self, logHandlers=[]):
        Platform.__init__(self, name='LINUX',
                          logHandlers=logHandlers)
        self.message_handlers['cfp-execute'] = self.create_task
        return

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

        name = proposition['tag']
        if 'queue' in proposition.keys():
            queueTag = proposition['queue']
        else:
            queueTag = None
        queueTag = proposition['queue']
        task = LINUXTask(name=name,
                         command=command,
                         sessionTag=proposition['tag'])
        self.submit(task, queue=queueTag)
        return

    def cancel_tasks(self, info):
        '''

        Handle message terminate experiment
        '''
        return


    def test_a(self):
        print 'Hello'



LINUX = LINUXPlatform()

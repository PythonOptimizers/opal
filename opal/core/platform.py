from mafrw import Agent
from mafrw import Message

class Task(Agent):
    def __init__(self,
                 name=None,
                 taskId=None,
                 command=None,
                 input=None,
                 output='/dev/null',
                 logHandlers=[]):
        '''

        Each task object correspond to an application of the target 
        algorithm on a test problem.

        '''
        self.task_id = taskId # task_id is assigned by platform
        self.command = command
        self.output=output
        if name is None:
            Agent.__init__(self, name=command, logHandlers=logHandlers)
        else:
            Agent.__init__(self, name=name, logHandlers=logHandlers)
        return

    def run(self):
        '''

        The common activity of all task is send a message that informs
        termination of its work
        '''
        message = Message(sender=self.id,
                          performative='inform',
                          receiver=None,
                          content={'proposition':{'who':self.name,
                                                  'what':'task-finish',
                                                  'how':'no-error'}
                                   }
                          )
        self.send_message(message)
        self.unregister()
        return
    
class Platform(Agent):
    def __init__(self,
                 name='platform',
                 maxTask=1,
                 synchronous=False,
                 logHandlers=[]):
        self.queue = []
        self.running = {}
        self.max_task = maxTask
        self.synchronous = synchronous
        self.task_id = 0
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        self.message_handlers['inform-task-finish'] = self.finalize_task
        return

    def submit(self, task):
        # A task is created by each platform
        task.register(self.environment)
        self.queue.append(task)
        self.logger.log('Task ' + task.name + ' is added to queue')
        return task.id
   
    def finalize_task(self, info):
        taskName = info['proposition']['who']
        del self.running[taskName]
        return

    def run(self):
        while self.working :
            if not self.synchronous or len(self.running) == 0: 
                # Submit task when there is no
                # running task
                #self.logger.log('Begin a launching session, we have ' + \
                #                str(len(self.queue)) + ' task')
                while (len(self.running) < self.max_task) and \
                          (len(self.queue) > 0):
                    task = self.queue.pop()
                    self.running[task.name] = task
                    task.start()
                    self.logger.log('Task: ' + str(task.name) + ' is launched')
                    #self.logger.log('We have ' + str(len(self.queue)) + \
                    #                ' task')
                    #self.logger.log('There are ' + \
                    #                str(self.max_task - len(self.running)) + \
                    #                ' available slot')
            # Work as an agent
            messages = self.fetch_messages()
            for msg in messages:
                self.handle_message(msg)
            del messages
        return
        

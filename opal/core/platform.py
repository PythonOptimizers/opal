from mafrw import Agent
from mafrw import Message

class Task(Agent):
    def __init__(self,
                 name=None,
                 taskId=None,
                 command=None,
                 sessionTag=None,
                 input=None,
                 output='/dev/null',
                 logHandlers=[]):
        '''

        Each task object correspond to an application of the target
        algorithm on a test problem.

        '''
        self.task_id = taskId # task_id is assigned by platform
        self.command = command
        self.output = output
        if name is None:
            Agent.__init__(self, name=command, logHandlers=logHandlers)
        else:
            Agent.__init__(self, name=name, logHandlers=logHandlers)
        if sessionTag is None:
            self.session_tag = self.name
        else:
            self.session_tag = sessionTag
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
        message = Message(sender=self.id,
                          performative='cfp',
                          receiver=None,
                          content={'action':'collect-result',
                                   'proposition':{'session-tag':self.session_tag}
                                   }
                          )
        self.send_message(message)
        self.unregister()
        return



class QueueSystem:
    # The default queue system managed the tasks in one or many queue
    # where each queue is identified by name
    def __init__(self):
        self.tasks = {'default':[]}
        return

    def get_length(self):
        length = 0
        for queueTag in self.tasks:
            length = length + len(self.tasks[queueTag])
        return length

    def append(self, task, queue=None):
        if (queue is None) or (queue is 'default'):
            self.tasks['default'].append(task)
        else:
            if queue in self.tasks.keys():
                self.tasks[queue].append(task)
            else:
                self.tasks[queue] = [task]
        return

    def pop(self, queue=None):
        if (queue is None) or (queue is 'default'):
            if len(self.tasks['default']) > 0 :
                return self.tasks['default'].pop()
            for queue in self.tasks.keys():
                if queue is not 'default':
                    return self.tasks[queue].pop()
            raise Exception('The task queue is empty')

        if queue in self.tasks.keys():
            task = self.tasks[queue].pop()
            # Remove the queue if it is empty
            if len(self.tasks[queue]) == 0:
                del self.tasks[queue]
            return task
        raise Exception('The task queue does not exist')


    def remove_tasks(self, queue=None):
        if (queue is None) or (queue is 'default'):
            del self.tasks['default'][0:]
            return
        if queue in self.tasks.keys():
            del self.tasks[queue]
            return
        return

class Platform(Agent):
    def __init__(self,
                 name='platform',
                 maxTask=1,
                 synchronous=False,
                 queueSystem=None,
                 settings=None,
                 logHandlers=[],
                 **kwargs):
        # A platform can contains many queues
        if queueSystem is None:
            self.queue_system = QueueSystem()
        else:
            self.queue_system = queueSystem
        self.settings = {'MAX_TASK':maxTask,
                         'SYNCHRONOUS':synchronous,
                         'OPTIONS':None}
        if settings is not None:
            self.settings.update(settings)
        self.settings.update(kwargs)

        # Running information
        self.running = {}
        self.task_id = 0
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        self.message_handlers['inform-task-finish'] = self.finalize_task
        self.message_handlers['cfp-cancel-queue'] = self.cancel_queue
        return

    def set_parameter(self, settings=None, **kwargs):
        if settings is not None:
            self.settings.update(settings)
        self.settings.update(kwargs)
        return

    def submit(self, task, queue=None):
        # A task is created by each platform
        task.register(self.environment)
        self.queue_system.append(task, queue)
        #self.logger.log('Task ' + task.name + ' is added to queue')
        return task.id

    def finalize_task(self, info):
        taskName = info['proposition']['who']
        del self.running[taskName]
        return

    def run(self):
        while self.working :
            if not self.settings['SYNCHRONOUS'] or len(self.running) == 0:
                # Submit task when there is no
                # running task
                #self.logger.log('Begin a launching session, we have ' + \
                #                str(len(self.queue)) + ' task')
                while (len(self.running) < self.settings['MAX_TASK']) and \
                          (self.queue_system.get_length() > 0):
                    task = self.queue_system.pop()
                    self.running[task.name] = task
                    task.start()
                    #self.logger.log('Task: ' + str(task.name) + ' is launched')
            # Work as an agent
            messages = self.fetch_messages()
            for msg in messages:
                self.handle_message(msg)
            del messages
        return

    # Message handlers

    def cancel_queue(self, info):
        if 'queue' in info['proposition'].keys():
            queueTag = info['proposition']['queue']
        else:
            queueTag = None
        self.queue_system.remove_tasks(queue=queueTag)
        return



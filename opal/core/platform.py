from mafrw import Agent
from mafrw import Broker

class Task(Agent):
    def __init__(self,
                 taskId=None,
                 command=None,
                 input=None,
                 output='/dev/null',
                 logHandlers=[]):
        '''

        Each task object correspond to an application of the target 
        algorithm on a test problem.

        '''
        self.task_id = taskId
        self.command = command
        Agent.__init__(self, logHandlers)
        return

    def run(self):
        return
    
class Platform(Broker):
    def __init__(self, maxTask=1, synchronous=True, logHandlers=[]):
        self.queue = []
        self.running = {}
        self.max_task = maxTask
        self.synchronous = synchronous
        self.task_id = 0
        Broker.__init__(self, logHandlers)
        return

    def submit(self, task):
        # A task is created by each platform
        self.add_agent(task)
        self.queue.append(task)
        return task.id
   
    def handle_message(self, message):
        # If the message is a request of task 
        # execution whose command is provided
        command = self.decrypt(message.content)
        self.submit_task(command)
        # Handle message that inform a task finishes its job
        taskId = self.decrypt(message.content)
        del self.running[taskId]
    

    def run(self):
        while self.alive :
            if not self.synchronuous or len(self.running) == 0: 
                # Submit task when there is no
                # running task
                while (len(self.running) < platform.max_task) and \
                        (len(self.queue) > 0):
                    task = self.queue.pop()
                    self.running.append(task)
                    task.start()
            # Work as an agent
            messages = self.fetch_message()
            for msg in messages:
                self.handle_message(msg)
        return
        

from mafrw import Agent

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
        self.task_id = taskId # task_id is assigned by platform
        self.command = command
        Agent.__init__(self, logHandlers)
        return

    def run(self):
        return
    
class Platform(Agent):
    def __init__(self, name='platform', maxTask=1, synchronous=True, logHandlers=[]):
        self.queue = []
        self.running = {}
        self.max_task = maxTask
        self.synchronous = synchronous
        self.task_id = 0
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        return

    def submit(self, task):
        # A task is created by each platform
        task.register(self.environment)
        self.queue.append(task)
        return task.task_id
   

    def run(self):
        while self.working :
            if not self.synchronous or len(self.running) == 0: 
                # Submit task when there is no
                # running task
                while (len(self.running) < self.max_task) and \
                        (len(self.queue) > 0):
                    task = self.queue.pop()
                    self.running.append(task)
                    task.start()
            # Work as an agent
            messages = self.fetch_messages()
            for msg in messages:
                self.handle_message(msg)
        return
        

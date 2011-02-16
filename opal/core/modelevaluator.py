import os
import sys
import os.path
import pickle
import log

#from opal.core.modelstructure import ModelEvaluator

__docformat__ = 'restructuredtext'


class ModelEvaluator(Broker):
    def __init__(self, model=None, logHandlers=[]):
        if model is None:
            self.data_manager = None
            self.task_manager = None
            self.structure_computer = None
        else:
            self.options = model.evaluating_options[]
            self.data_manager = DataManager(rows=model.data.get_problems(),
                                            columns=model.data.get_measures())
            self.task_manager = TaskManager(algorithm=model.dat.get_algorithm(),
                                            problems=model.data.get_problems(),
                                            platform=model.options['Platform'])
            self.structure_computer = StructureComputer()
        return

    def run(self):
        # Exit immediately if one of the agent is not defined
        if (self.data_manager is None) or \
                (self.task_manager is None) or \
                (self.structure_computer is None):
            return
        # Activate the agents
        self.data_manager.start()
        self.task_manager.start()
        self.taks_manager.start()
        # Wait until all of agents finish
        self.data_manager.join()
        self.task_manager.join()
        self.taks_manager.join()
        # We expect that, after all of agents finish their works, 
        # there is at least one message whose content contains 
        # model values in the messages queue of ModelEvaluator
        return

  
   

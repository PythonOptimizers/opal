import os
import sys
import os.path
import pickle
import log

from .mafrw import Broker
from .datamanager import DataManager
from .experimentmanager import ExperimentManager

#from opal.core.modelstructure import ModelEvaluator

__docformat__ = 'restructuredtext'


class ModelEvaluator(Broker):
    def __init__(self, 
                 model=None, 
                 modelFile=None,
                 logHandlers=[]):
        if model is None:
            if modelFile is None:
                self.data_manager = None
                self.task_manager = None
                self.structure_computer = None
                return
            else:
                # The model is loaded by pickling
                # Be able to be serialized is a requirement for
                # a model object
                f = open(modelFile)
                model = pickle.load(f)
                f.close()
    
        self.options = model.evaluating_options
        self.data_manager = DataManager(rows=model.get_problems(),
                                        columns=model.get_measures())
        self.experiment_manager = ExperimentManager(algorithm=model.get_algorithm(),
                                                    problems=model.get_problems(),
                                                    platform=model.evaluating_options['platform'])
        self.structure_computer = StructureComputer(structure=model.model_structure)
        return

    def initialize(self):
        # Exit immediately if one of the agent is not defined
        if (self.data_manager is None) or \
                (self.experiment_manager is None) or \
                (self.structure_computer is None):
            return
        # Register the agents
        self.add_agent(self.data_manage)
        self.add_agent(self.experiment_manager)
        self.add_agent(self.structure_computer)
        # Activate the agents
        self.data_manager.start()
        self.experiment_manager.start()
        self.structure_computer.start()
      
        return
       
    def handle_message(self, message):
        '''

        Handle message contains parameter values to provoke 
        an evaluation 
        '''
        paramValues = self.decrypt(message.content)
        self.add_message()
        return
    
    def finalize(self):
        # Wait until all of agents finish
        self.data_manager.join()
        self.experiment_manager.join()
        self.structure_computer.join()
        # We expect that, after all of agents finish their works, 
        # there is at least one message whose content contains 
        # model values in the messages queue of ModelEvaluator
        return

      
  
   

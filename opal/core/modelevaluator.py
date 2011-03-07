import os
import sys
import os.path
import pickle
import log

from .mafrw import Broker
from .datamanager import DataManager
from .experimentmanager import ExperimentManager
from .structcomp import StructureComputer
from ..Platforms import supported_platforms

#from opal.core.modelstructure import ModelEvaluator

__docformat__ = 'restructuredtext'


class ModelEvaluator(Broker):
    def __init__(self, 
                 name='model evaluator',
                 model=None, 
                 modelFile=None,
                 options={},
                 logHandlers=[]):
        Broker.__init__(self, name=name, logHandlers=logHandlers)
        if model is None:
            if modelFile is None:
                self.data_manager = None
                self.experiment_manager = None
                self.structure_computer = None
                self.platform = None
                return
            else:
                # The model is loaded by pickling
                # Be able to be serialized is a requirement for
                # a model object
                f = open(modelFile)
                model = pickle.load(f)
                f.close()
    
        self.options = {'platform': 'LINUX', 
                        'synchronized': True,
                        'interruptible': False}
        self.options.update(options)
        self.options.update(model.evaluating_options)
        self.data_manager = DataManager(rows=model.get_problems(),
                                        columns=model.get_measures())
        self.experiment_manager = ExperimentManager(algorithm=model.get_algorithm(),
                                                    problems=model.get_problems())
        # if platform option is provided by a string representing the name of 
        # a OPAL-supported platform
        if type(self.options['platform']) == type('a string'):
            plfName = self.options['platform']
            self.platform = supported_platforms[plfName]
        else:  # Platform is specified by a Platform-subclassed object
            self.platform = self.options['platform']

        self.structure_computer = StructureComputer(structure=model.structure)
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

      
  
   

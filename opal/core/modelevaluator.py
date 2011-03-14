import os
import sys
import os.path
import pickle
import log

from .mafrw import Agent
from .datamanager import DataManager
from .experimentmanager import ExperimentManager
from .structcomp import StructureComputer
from ..Platforms import supported_platforms

#from opal.core.modelstructure import ModelEvaluator

__docformat__ = 'restructuredtext'


class ModelEvaluator(Agent):
    def __init__(self, 
                 name='model evaluator',
                 model=None, 
                 modelFile=None,
                 options={},
                 logHandlers=[]):
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        self.options = {'platform': 'LINUX', 
                        'synchronized': True,
                        'interruptible': False}
        self.options.update(options)
        if model is None:
            if modelFile is not None:
                # The model is loaded by pickling
                # Be able to be serialized is a requirement for
                # a model object
                f = open(modelFile)
                model = pickle.load(f)
                f.close()
           
        self.model = model
        self.options.update(self.model.evaluating_options)
       
        # if platform option is provided by a string representing the name of 
        # a OPAL-supported platform
        
        return

    def parse_message(self, message):
        cmd = Agent.parse_message(self, message)
        if cmd in self.message_handlers.keys():
            return cmd
        cmd = message.performative + message.content['action']
        return cmd

    def register(self, environment):
        '''

        After adding his name in the environment database, it will look for 
        the agents that work as data manager, experiment manager and structure computer.
        If it could not find one of these agents within environment, it will 
        create them and let them register to environment

        The find process is realized by sending a test message to environment and wait
        for replying.
        '''
        Agent.register(self, environment)
        
        if self.model is None:
            return
        
        if self.find_collaborator('data manager',environment) is None:
            data_manager = DataManager(rows=self.model.get_problems(),
                                       columns=self.model.get_measures())
            data_manager.register(environment)
        
        if self.find_collaborator('exeperiment manager', environment) is None:
            experiment_manager = ExperimentManager(algorithm=self.model.get_algorithm(),
                                                   problems=self.model.get_problems(),
                                                   platform=self.options['platform'])
            experiment_manager.register(environment)

        if self.find_collaborator('structure computer', environment) is None:
            structure_computer = StructureComputer(structure=self.model.structure)
            structure_computer.register(environment)

        return
    
    def find_collaborator(self, name, environment):
        return None

    
      
  
   

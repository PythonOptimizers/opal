import os
import sys
import os.path
import pickle
import log
import hashlib

from .mafrw import Agent
from .mafrw import Message
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
                        'synchronized': False,
                        'interruptible': True}
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

        self.message_handlers['cfp-evaluate-point'] = \
                                            self.activate_parameter_evaluation
        self.message_handlers['inform-experiment-failed'] = \
                                                          self.experiment_failed
        return

    def register(self, environment):
        '''

        After adding his name in the environment database, it will look for     
        the agents that work as data manager, experiment manager and structure
        computer.
        If it could not find one of these agents within environment, it will 
        create them and let them register to environment

        The find process is realized by sending a test message to environment
        and wait for replying.
        '''
        Agent.register(self, environment)
        
        if self.model is None:
            return
        
        #if self.find_collaborator('data manager',environment) is None:
        #    data_manager = DataManager(rows=self.model.get_problems(),
        #                               columns=self.model.get_measures())
        #    data_manager.register(environment)
        
        if self.find_collaborator('exeperiment manager', environment) is None:
            experiment_manager =\
                        ExperimentManager(algorithm=self.model.get_algorithm(),
                                          problems=self.model.get_problems(),
                                          platform=self.options['platform'])
            experiment_manager.register(environment)

        if self.find_collaborator('structure computer', environment) is None:
            structure_computer = \
                               StructureComputer(structure=self.model.structure,
                                                 problems=\
                                                 self.model.get_problems(),
                                                 measures=\
                                                 self.model.get_measures())
            structure_computer.register(environment)

        return
    
    def find_collaborator(self, name, environment):
        return None

    def create_tag(self, point):
        valuesStr = '_'
        for coordinate in point:
            valuesStr = valuesStr + str(coordinate) + '_'
        return hashlib.sha1(valuesStr).hexdigest()
  
    # Message handlers

    def activate_parameter_evaluation(self, info):
        parameterValues = info['proposition']['point']
        if 'tag' in info['proposition'].keys():
            parameterTag = info['proposition']['tag']
        else:
            parameterTag = self.create_tag(parameterValues)

        message = Message(sender=self.id,
                          performative='cfp',
                          content={'action':'evaluate-parameter',
                                   'proposition':{'parameter':parameterValues,
                                                  'tag':parameterTag}
                                   })
        self.send_message(message)
        return

    def experiment_failed(self, info):
        paramTag = info['proposition']['parameter-tag']
        message = Message(sender=self.id,
                          performative='inform',
                          content={'proposition':{'what':'model-value',
                                                  'values':None,
                                                  'why':'parameters invalid',
                                                  'parameter-tag':paramTag
                                                  }
                                   })
        self.send_message(message)
        return

    def stop_expriment(self, info):
        paramTag = info['proposition']['parameterTag']
        log.debugger.log('There is a request to stop experiment')
        return
        
      
  
   

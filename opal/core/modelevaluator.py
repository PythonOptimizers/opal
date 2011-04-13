import os
import sys
import os.path
import pickle
import log
import hashlib

from .mafrw import Agent
from .mafrw import Message
from .datagenerator import DataGenerator
from .structureevaluator import StructureEvaluator
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
                                                  self.handle_experiment_failed
        self.message_handlers['inform-objective-partially-exceed'] = \
                                                  self.estimate_partially_model
        self.message_handlers['inform-constraint-partially-violated'] = \
                                                  self.estimate_partially_model
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
        
        # Find the neccessary collaborators. If could find it, create the
        # predefinded collaborators
        
        if self.find_collaborator('data generator', environment) is None:
            dataGenerator =\
                       DataGenerator(algorithm=self.model.get_algorithm(),
                                     parameters=self.model.get_parameters(),
                                     problems=self.model.get_problems(),
                                     platform=self.options['platform'])
            dataGenerator.register(environment)

        if self.find_collaborator('structure evaluator', environment) is None:
            structureEvaluator = \
                          StructureEvaluator(structure=self.model.structure,
                                            problems=self.model.get_problems(),
                                            measures=self.model.get_measures())
            structureEvaluator.register(environment)

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

    def handle_experiment_failed(self, info):
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

    def estimate_partially_model(self, info):

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
        
      
  
   

import os
import string
import types
import time
import shutil
import log
import copy
import threading
import hashlib
#import logging

#import utility
from testproblem import TestProblem
from data import Data
from mafrw import *

from platform import Platform
from ..Platforms import supported_platforms

from .. import config

        
class DataGenerator(Agent):
    """ 
    
    This class represents a data generator for a parameter optimization
    problem. The data is the values of the elementary measures that are needed
    to formulate the problem. To specify a data generator, we need provide:

    1. The algorithm wrapper
    2. the set of elementary measures concerned 
    3. the set of parameters to control
    4. the test problems set.
    """

    def __init__(self, 
                 name='data generator',
                 algorithm=None, 
                 parameters=None,
                 measures=None,
                 problems=[],
                 platform=None,
                 logHandlers=[], 
                 options={},
                 **kwargs):
        
        # The core variables
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        self.algorithm = algorithm
        if parameters is None: # No parameter subset is specified
            self.parameters = algorithm.parameters # All parameters of algorithm
                                                 # is considered
        else:
            self.parameters = parameters

        #log.debugger.log(str([(param.name, param.kind) \
        #                      for param in self.parameters]))
            
        if measures is None: # No measure subset is specified
            self.measures = algorithm.measures # All measures of algorithm is
                                             # is considered
        else:
            self.measures = measures

        if (problems is None) or (len(problems) == 0): # No test problem is 
                                                       # is specified,
                                                       # algorithm can be run 
                                                       # without 
                                                       # indicating problem
            self.problems = [TestProblem(name='TESTPROB')] # A list of one 
                                                           # one problem is
                                                           # is created
        else:
            self.problems = problems

        self.platform_description = platform
        
        self.options = {'interruptible':True}
        if options is not None:
            self.options.update(options)
        self.options.update(kwargs)

        #self.platform = platform
        
        
        # By default, logger is Logger object of Python's logging module
        # Logger is set name to modeldata, level is info.
        # self.logger = log.OPALLogger(name='modelData', handlers=logHandlers)
      
        self.experiments = {} # List of all experiements in executions
        self.message_handlers['cfp-evaluate-parameter'] = self.run_experiment
        self.message_handlers['inform-task-finish'] = self.get_result
        self.message_handlers['inform-objective-partially-exceed'] = \
                                                     self.terminate_experiment
        self.message_handlers['inform-constraint-partially-violated'] = \
                                                     self.terminate_experiment
        return

    def register(self, environment):
        Agent.register(self, environment)
        if self.find_platform(self.platform_description, environment) is None:
            platform = self.create_platform()
            platform.register(environment)
        return

  
    #  Private method
    def update_parameter(self, values):
        for (param, val) in zip(self.parameters, values):
            #log.debugger.log(str((param.name, param.kind)))
            param.set_value(val)
        return 

    def create_tag(self):
        valuesStr = '_'
        for param in self.parameters:
            valuesStr = valuesStr + param.name + ':' + str(param.value) + '_'
        return hashlib.sha1(valuesStr).hexdigest()
  
    def find_platform(self, platformName, environment):
        return None

    def create_platform(self):
        if self.platform_description['name'] in supported_platforms:
            platform = supported_platforms[self.platform_description['name']]
            try:
                settings = self.platform_description['settings']
                platform.set_parameter(**settings)
            except:
                pass # Do nothing, leave the platform with default setting
            return platform
        # Could not find a supported platform by the name, create a Platform
        # object
        platform = Platform(name=self.platform_description['name'],
                            settings=self.platform_description['settings'])
        return platform
        
    # Message handlers
    def run_experiment(self, info=None):
        '''

        Handle a cfp message that call for a proposal
        of scoring algorthim at a parameter point
        '''
        if info is None:
            return
        
        parameterValues = info['proposition']['parameter']
        self.update_parameter(parameterValues)
        if 'tag' in info['proposition'].keys():
            parameterTag = info['proposition']['tag']
        else:
            parameterTag = self.create_tag()
        # If the parameters are invalid, send a message informing the
        # experiment is failed
        if not self.algorithm.are_parameters_valid():
            message = Message(sender=self.id,
                              performative='inform',
                              content={'proposition':\
                                       {'what':'experiment-failed',
                                        'why':'invalid-parameters',
                                        'parameter-tag':parameterTag}
                                       }
                              )
            self.send_message(message)
            return
        # Otherwise, for each problem, send a cfp message that propose execute
        # the algorithm. The content of message is the execution command
        for prob in self.problems:
            # Get the elements relating execution of an experiment
            cmd, paramFile, outputFile, sessionTag = \
                 self.algorithm.solve(problem=prob,
                                      parameters=self.parameters,
                                      parameterTag=parameterTag)
            # Update the experiment database
            self.experiments[sessionTag] = {'parameter-tag':parameterTag,
                                            'parameter-file': paramFile,
                                            'output-file':outputFile,
                                            'problem-name':prob.name}
            # Create a message having intention of provoking the command of
            # solving the test problem by algorithm
            message = Message(sender=self.id,
                              performative='cfp',
                              content={'action':'execute',
                                       'proposition':{'command':cmd,
                                                      'tag':sessionTag,
                                                      'queue':parameterTag}}
                              )
            self.send_message(message)
        return

    def terminate_experiment(self, info):
        paramTag = info['proposition']['parameter-tag']
        message = Message(sender=self.id,
                          performative='cfp',
                          content={'action':'cancel-queue',
                                   'proposition':{'queue':paramTag}
                                   }
                          )
        self.send_message(message)
        return
    
    def get_result(self, info=None):
        '''

        Handle the message that informs a solving session is terminated.
        The content message contains information of identifying the
        terminated session 
        '''
        if 'proposition' not in info.keys():
            return
        proposition =  info['proposition']
        sessionTag = proposition['who']
        exprInfo = self.experiments[sessionTag]
        outputFile = exprInfo['output-file']
        problem = exprInfo['problem-name']
        paramTag = exprInfo['parameter-tag']
        paramFile = exprInfo['parameter-file']
        measureValues = self.algorithm.read_measure(outputFile)
        message = Message(sender=self.id,
                          performative='inform',
                          content={'proposition':{'what':'measure-values',
                                                  'values':measureValues,
                                                  'parameter-tag':paramTag,
                                                  'problem':problem}
                                   }
                          )
        self.send_message(message)
        # Remove the information entry
        del self.experiments[sessionTag]
        # Remove the parameter file
        if os.path.exists(paramFile):
            os.remove(paramFile)
        # Remove the measure file
        if os.path.exists(outputFile):
            os.remove(outputFile)
        return
        
        

import os
import string
import types
import time
import shutil
import log
import copy
import threading
#import logging

#import utility
from measure import MeasureValueTable
from testproblem import TestProblem
from data import Data
from mafrw import *

from .. import config

class Experiment(Data):
    '''

    Contains information, status of an experiment
    '''
    def __init__(self):
        return
        
class ExperimentManager(Broker):
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
                 algorithm, 
                 parameters=None, measures=None,
                 problems=[],
                 interruptible=False, 
                 logHandlers=[], 
                 **kwargs):
        
        # The core variables
        self.algorithm = algorithm
        if parameters is None: # No parameter subset is specified
            self.parameters = algorithm.parameters # All parameters of algorithm
                                                 # is considered
        else:
            self.parameters = parameters

        if measures is None: # No measure subset is specified
            self.measures = algorithm.measures # All measures of algorithm is
                                             # is considered
        else:
            self.measures = measures

        if (problems is None) or (len(problems) == 0): # No test problem is 
                                                       # is specified, algorithm 
                                                       # can be run without 
                                                       # indicating problem
            self.problems = [TestProblem(name='TESTPROB')] # A list of one 
                                                           # one problem is
                                                           # is created
        else:
            self.problems = problems
        
        #self.platform = platform
        
        
        # By default, logger is Logger object of Python's logging module
        # Logger is set name to modeldata, level is info.
        self.logger = log.OPALLogger(name='modelData', handlers=logHandlers)
      
        self.experiments = {} # List of all experiements in executions
        return

    def get_parameters(self):
        return self.parameters

    def create_experiment_id(self, parameterValues):
        valuesStr = '_'
        j = 0
        for i in range(len(self.parameters)):
            self.parameters[i].set_value(parameterValues[j])
            valuesStr = valuesStr + str(parameterValues[j]) + '_'
            j = j + 1    
        return str(hash(valuesStr))

    
    def run_experiment(self, parameterValues):
        # Prepare all neccessary things likes working directory
        # create id, create parameter file ..
        experimentId = self.create_experiment_id(parameterValues)
        for prob in self.problems:
            msgContent = self.encrypt(self.algorithm.solve(parameterFile, problem))
            message = Message(sender=self.id,
                              performative='REQ',
                              content=msgContent)
            self.send_message(message)
        
    def message_handle(self, message):
        # If request message is a request of executing target algorithm 
        # with parameter values encrypted in the message
        parameterValues = self.decrypt(message.content)
        self.run_exeperiment(parameterValues)
        return

    def fetch_messages(self, environment=None):
        """
        
        Data generator concentrate only the following message types:
        - Request to generate a new data corresponding a set of parameter value.
          This request comme from particularly a data controller that want new 
          data to add to his database
        - Signal to inform to stop. 
        """ 
        
        requests = []
        return requests

    def descrypt(self, message):
        """
        
        Data generator decrypts a request to get the parameter values or 
        decrypt a signal 
        """
        parameterValues = []
        return parameterValues

   

        
        

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

from .. import config

class TaskManager(Broker):
    """ 
    This class represents a data generator for a parameter optimization
    problem. The data is the values of the elementary measures that are needed
    to formulate the problem. To specify a data generator, we need provide:

    1. The algorithm wrapper
    2. the set of elementary measures concerned 
    3. the set of parameters to control
    4. the test problems set.
    """

    def __init__(self, wrapper, parameters=None, measures=None,
                 problem=[],
                 platform=config.platform, synchronous=True, interruptible=False, 
                 logHandlers=[], **kwargs):
        # The core variables
        self.wrapper = wrapper
        if parameters is None: # No parameter subset is specified
            self.parameters = wrapper.parameters # All parameters of wrapper
                                                 # is considered
        else:
            self.parameters = parameters

        if measures is None: # No measure subset is specified
            self.measures = wrapper.measures # All measures of wrapper is
                                             # is considered
        else:
            self.measures = measures

        if (problems is None) or (len(problems) == 0): # No test problem is 
                                                       # is specified, wrapper 
                                                       # can be run without 
                                                       # indicating problem
            self.problems = [TestProblem(name='TESTPROB')] # A list of one 
                                                           # one problem is
                                                           # is created
        else:
            self.problems = problems
        
        self.platform = platform

        # By default, logger is Logger object of Python's logging module
        # Logger is set name to modeldata, level is info.
        self.logger = log.OPALLogger(name='modelData', handlers=logHandlers)
        # The monitor variables
        self.test_number = 0
        self.test_id = None

        # The output
        self.test_is_failed = False
        pNames = [prob.name for prob in self.problems]
        mNames = [measure.name for measure in self.measures]
        self.measure_value_table = MeasureValueTable(problem_names=pNames,
                                                     measure_names=mNames)
        # Set options

        #self.set_options(**kwargs)
        return

    def get_parameters(self):
        return self.parameters


    def initialize(self, parameterValues):
        '''
        
        This method return an unique identity for the 
        test basing on the parameter values
    
        The identity obtains by hashing the parameter values string. 
        This is an inversable function. It means that we can get 
        the parameter_values form the id
        '''
        
        valuesStr = '_'
        j = 0
        for i in range(len(self.parameters)):
            self.parameters[i].set_value(parameterValues[j])
            valuesStr = valuesStr + str(parameterValues[j]) + '_'
            j = j + 1    
        self.test_id = str(hash(valuesStr))
        self.test_number += 1
        self.test_is_failed = False
        #self.measure_value_table.clear()
        self.data_controller.start()
        self.logger.log('Initialize the ' + str(self.test_number) + \
                         ' test with id ' + str(self.test_id))
        self.logger.log(' - Parameter values: ' + valuesStr.replace('_', ' ')) 
        return 

    def finalize(self):
        #self.wrapper.clean_running_data(testId=self.test_id)
        self.data_controller.stop()
        self.logger.log('Finalize the test ' + str(self.test_id))
        return

    def generate_data(self, parameterValues):
        self.initialize(parameterValues=parameterValues)
        #print '[modeldata.py]',[param.value for param in self.parameters]
        self.logger.log('Run the test ' + str(self.test_id))
        self.wrapper.set_parameter(parameters=self.parameters, 
                                     testId=self.test_id)
        if not self.wrapper.are_parameters_valid():
            #print '[modeldata.py]','Parameter values are invalid, test fails'
            self.test_is_failed = True
            self.logger.log(' - The parameter values are invalid, ' + \
                             'the test is stopped')
            return
        
        self.platform.initialize(self.test_id)
        self.logger.log(' - Solve the test problems')
        probIndex = 0
        while True: # Enter the main loop of launching 
            if self.synchronous: # If data generator works in synchronous mode,
                                 # it have to wait for all previous submitted 
                                 # tasks finish to launch the new tasks
                while (platform.get_running_tasks() > 0): # Platform is ready for new submits
                    if self.stop_signal: # Check if any stop signal is recevied and
                                         # is in processing, do not lauch any more 
                                         # a task 
                    break # escape from waiting for the platform is ready
            if self.stop_signal:
                break # break from main loop of launching
            # Launch the tasks 
            while (probIndex < len(self.problems)) and \ # Check if there is a task to submit
                    (platform.is_ready()): # Check availbility of plaform
                self.platform.submit(\
                    self.wrapper.run(problem=self.problems[probIndex], 
                                     testId=self.test_id))
                probIndex++
       
       
        self.logger.log(' - All problems are solved, the test is stopped')
        
    def run(self):
        self.initialize()
        while self.stop_signal is None:
            self.requests = self.fetch_messages()
            for req in self.requests:
                self.request_handle(req)
               
        # After exitting from the loop of launching, data generator will 
        # wait for all tasks finish to finailize a working session
        self.platform.finalize()
        self.finalize()
        return 
    
    def request_handle(self, message):
        # If request message is a request of executing target algorithm 
        # with parameter values encrypted in the message
        parameterValues = self.decrypt(req)
        self.generate_data(parameterValues)
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

   

        
        

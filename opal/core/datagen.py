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


# =============================
class DataGenerator(Broker):
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
                 wrapper, 
                 problem=[],
                 platform=config.platform, 
                 synchronous=True, 
                 interruptible=False, 
                 logHandlers=[]):
        # The core variables
        self.wrapper = wrapper
    
        self.problems = problems
        
        self.platform = platform

        # By default, logger is Logger object of Python's logging module
        # Logger is set name to modeldata, level is info.
        self.logger = log.OPALLogger(name='modelData', handlers=logHandlers)
        # The monitor variables
        self.request_id = {} # This variables store a map the test id and 
                             # requestor id

        return

    def finalize(self):
        #self.wrapper.clean_running_data(testId=self.test_id)
        self.data_controller.stop()
        self.logger.log('Finalize the test ' + str(self.test_id))
        return

    def generate_data(self, parameterValues, runId):
        self.initialize(parameterValues=parameterValues)
        #print '[modeldata.py]',[param.value for param in self.parameters]
        self.logger.log('Run the test ' + str(self.test_id))
        self.wrapper.set_parameter(parameterValues=self.parameterValues, 
                                   testId=runId)
        # The parameter values are not valid
        if not self.wrapper.are_parameters_valid():
            # Send a signal to indicate that no test is executed
            msg = Message(performative='SIG',
                          sender=self.agent_name,
                          content=self.encypt(data=Non),
                          reference=self.
                          
            self.stop_signal = True
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
        while True:
            messages = self.fetch_messages()
            while len(messages) > 0:
                msg = messages.pop()
                self.handle_message()
                parameterValues = self.decrypt(msg)
                self.generate_data(parameterValues)
        # After exitting from the loop of launching, data generator will 
        # wait for all tasks finish to finailize a working session
        self.platform.finalize()
        self.finalize()
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

    def decrypt(self, msgContent):
        """
        
        Data generator decrypts a request to get the parameter values or 
        decrypt a signal 
        """
        parameterValues = []
        return parameterValues

    def handle_message(self, message):
        # This is a data request 
        if message.performative == 'REQ':
            parameterValues = decrypt(message.content)
            runId = self.get_id(parameterValues)
            self.request_id[message]
        

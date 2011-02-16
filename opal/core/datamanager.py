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

# =============================

class DataManager(Agent):
    """
    
    An object of this class is responsable to collect data, 
    support access to data of a test corresponding to one set 
    of parameter

    During a session working of data generator, it is activated 
    at first, wait for signal of a task to collect the data and
    store data following its rules. Normally, the data is stored 
    in external memory (for example a file) but a part can be loaded 
    into memory (a variable of DataController object).

    The other components needing data sends to this object a 
    request and get the data.
    """
    def __init__(self, 
                 rows=None,
                 column=None,
                 storage=None):
        self.file_name = 'data_storage.txt'
        self.requests = []
        self.events = []
        self.stop_signal = False
        return

    def reply_request(self, request):
        return

    def handle_message(self, message):
        # If message is a data request
        if message.performative == 'REQ':
            # Decrypt message content to get the parameter values
            # and problem name
            (paramValues, problem) = self.decrypt(message)
            # Get data from the measures
            measureValues = self.get_data()
            # If getting data is successful
            if measureValues is not None:
                # Create a reply message whose content contains the 
                # measure values
                msgCont = self.encrypt(measureValues)
                msg = Message(sender=self.name,
                              content=msgCont,
                              performative='REP',
                              reference=message.id)
        # If message is a signal indicating a task is completed and 
        # the outputed measure values file is available
        elif message.performative == 'SIG':
            # Decrypt the content of SIG
            (paramValues, problem, measureFile) = self.decrypt(message):
            id = self.get_id(parameterValues)
            # Collect the measure values from output file 
            measureValues = self.collect_data(measureFile)
            if measureValues is not None:
                # Collect sucessfully, add to the storage
                self.add_data(id, problem, measureValues)
           
        return

    def get_data(self, parameterValues, dataId=None):
        if dataId is None:
            dataId = self.get_id(parameterValues)
        return self.storage[dataId]
    

    def fetch_messages(self):
        return messages
    def collect_data(self, problem, measureFile):
         measure_values = self.wrapper.get_measure(prob, self.test_id)
            if measure_values is None: # Some error in running the wrapper, 
                                       # so we could not get the meaure
                self.finalize()
                return None
            #print measure_values
            if len(measure_values) == 0: # Some error in getting the measure, 
                                         # so we could not get the meaure
                self.finalize()
                return TestResult(testIsFailed=True) 
            self.measure_value_table.add_problem_measures(prob.name,measure_values)
        return

    def run(self):
        while not self.stop_signal:
            messages = self.fetch_messages()
            while len(messages) > 0:
                msg = messages.pop()
                self.handle_messages(msg)
                
                self.send(requestor, data)
            pass
        return


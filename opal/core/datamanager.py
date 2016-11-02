import os
import string
import types
import time
import shutil
import log
import copy
#import logging

#import utility
from testproblem import TestProblem
from mafrw import Agent

from .. import config


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
                 name='data manager',
                 rows=None,
                 columns=None,
                 storage=None,
                 logHandlers=[]):
        self.file_name = 'data_storage.txt'
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        self.message_handlers['inform-measure-values'] = self.add_data
        self.message_handlers['cfp-collect'] = self.collect_data
        return

    # Management functionality
    def update(self, problem, parameterTag, data):
        return

    def find(self, query):
        return

    # Message handlers
    def add_data(self, info):
        if info is None:
            return

        paramTag = info['proposition']['parameter-tag']
        prob = info['proposition']['problem']
        data = info['proposition']['values']
        # Update the entry
        self.update(parameterTag=paramTag,
                    problem=prob,
                    data=data)
        # Get all data entry corresponding to the tag
        dataEntry = self.find(self, query={'tag':paramTag})
        # Send a message informing availbility of data
        if dataEntry.is_complete():
            msg = Message(sender=self.id,
                          performative='inform',
                          content={'proposition':{'what':'data-availability',
                                                  'how':'complete',
                                                  'data':dataEntry}
                                   }
                      )
        else:
            msg = Message(sender=self.id,
                          performative='inform',
                          content={'proposition':{'what':'data-availability',
                                                  'how':'partial',
                                                  'data':dataEntry}
                                   }
                      )
        self.send_message(msg)
        return

    def find_data(self, info):

        (paramValues, problem) = message.content['proposition']
        measureValues = self.query_data(parameters=paramValues,
                                        problem=problem)
        # If getting data is successful
        if measureValues is not None:
            # Create a reply message whose content contains the
            # measure values
            msgCont = self.encrypt(measureValues)
            msg = Message(sender=self.id,
                          content=msgCont,
                          performative='inform',
                          reference=message.id)
        return

    def collect_data(self, message):
        (paramValues, problem, measureFile) = message.content['proposition']
        f = open(measureFile)
        f.close()
        return

    # Private methods
    def query_data(self, parameters=None, problem=None):
        return None

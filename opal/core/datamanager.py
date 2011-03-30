import os
import string
import types
import time
import shutil
import log
import copy
#import logging

#import utility
from measure import MeasureValueTable
from testproblem import TestProblem
from mafrw import Agent

from .. import config

# =============================

class ExperimentResult(DataTable):
    '''

    An ExperimentResult contains information about the result of an experiment.
    Each object is identified by an id (name or tag) formed by parameter values.

    The information includes at least:

      1. Parameter values
      2. A flag indicating the experiment failed or not
      3. A flog indicating the measure table is complete or not
    '''
    def __init__(self, name, problems, measures):
        self.problems = problems
        self.measures = measures
        rowIds = [prob.identify() for prob in problems]
        colIds = [measure.identify() for measure in measures]
        DataTable.__init__(name, rowIds, colIds)
        return
    
    def __len__(self):
        return DataTable.__len__(self)

    def __getitem__(self, key):
        '''

        For supporting the operations on the measure to build up
        composite measures, this operator on a measure table is changed
        slightly. It now accepts a key of two possible forms:
        (problem, measure) or (measure). In both of case, it return a
        Data object. The differences are:
    
        In the first case, is return a scalar with name combined from,
        problem identity (name), measure identity (name) and experiment
        identity (name).
        '''
        
        if type(key) == type(('Problem','Measure')):
            return self.get_cell(key[0],key[1])
        return self.get_column(key)


    def get_cell(self, prob, measure):
        #print prob,measure,self.table[measure],self.problem_indices[prob]
        if type(prob) == type(self.problems[0]):
            probId = prob.identify()
        elif type(prob) == type(self.problems[0].identify()):
            probId = prob
        else:
            raise Exception('Problem identity is not valid')
        
        if type(prob) == type(self.problems[0]):
            probId = prob.identify()
        elif type(prob) == type(self.problems[0].identify()):
            probId = prob
        else:
            raise Exception('Problem identity is not valid')
        cell = Data(name=
        return self.table[problem][measure]

    def get_column(self,measure):
        col = []
        for prob in sorted(self.problem_names):
            col.append(self.table[prob][measure])
        try:
            import numpy
            return numpy.array(col)
        except ImportError:
            import array
            return array.array('d', col)

    def get_row(self,prob):
        row = []
        for measure in sorted(self.measure_names):
            row.append(self.table[prob][measure])
        return row

    def get_problems(self):
        return sorted(self.problem_names)

    def get_measures(self):
        return sorted(self.measure_names)

    def add_problem_measures(self,problem,measure_values):
        #self.problem_indices[problem] = len(self.problem_indices)
        #print problem,measure_values
        self.table[problem] = copy.copy(measure_values)
        return

    def clear(self):
        for problem in self.table.keys():
            del self.table[problem]
        return

    def __str__(self, formatter=TableFormatter()):
        #print self.table
        #print self.problem_indices
        #print self.measure_names
        return self.toString(formatter=formatter)


    def toString(self, formatter=TableFormatter()):
        tableStr = ''
        headerStr = formatter.set_header(headers=self.measure_names)
        if headerStr is None:
            return None
        tableStr = tableStr + headerStr
        for prob in sorted(self.table.keys()):
            recordStr = formatter.format(prob, self.table[prob])
            if recordStr is not None:
                tableStr = tableStr + recordStr
        return tableStr
    

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

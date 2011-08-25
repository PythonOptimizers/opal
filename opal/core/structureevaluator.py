import sys
import os.path
import marshal
import new
import log

from mafrw import Agent
from mafrw import Message

from set import Set
from data import DataTable


class DataCacheEntry(DataTable):
    def __init__(self, name, parameters, problems, measures):
        self.parameters = parameters
        DataTable.__init__(self,
                           name=name,
                           rowIdentities=problems,
                           columnIdentities=measures)
        return

    def identify(self):
        return self.name

    def get_measure_vector(self, measure):
        '''

        Return Data Set object
        '''
        valDict = self.get_column(measure)
        valVect = []
        for prob in self.get_row_keys():
            if prob in valDict.keys():
                valVect.append(valDict[prob])
        return valVect

class DataCache(Set):
    def __init__(self, name, problems, measures):
        self.problems = problems
        self.measures = measures
        Set.__init__(self, name)
        return

    def create_entry(self, paramTag, parameterValues):
        entry = DataCacheEntry(name=paramTag,
                               parameters=parameterValues,
                               problems=[prob.identify() \
                                         for prob in self.problems],
                               measures=[measure.identify() \
                                         for measure in self.measures])
        self.append(entry)
        
    def get_parameters(self, paramTag):
        entry = self.__getitem__(paramTag)
        return entry.parameters

    def get_measure_vectors(self, paramTag):
        '''

        Return a dictionary of measure vectors. The keys are measure names
        '''
        measures = {}
        entry = self.__getitem__(paramTag)
        measureIds = [m.identify() for m in self.measures]
        for measureId in measureIds:
            measures[measureId] = entry.get_measure_vector(measureId)
        return entry.get_storage_ratio(), measures
       
    

class StructureEvaluator(Agent):
    """
    
    An object of this class represent for the model structure that is 
    described in Python language. The evaluator accept only ModelStructure 
    object as structure of model. Any structure modeled by other language 
    such as AMPL has to be rewritten as a ModelStructure object. This 
    can be done by the interpreters.
    """
    def __init__(self,
                 name='structure evaluator',
                 structure=None,
                 problems=None,
                 measures=None,
                 logHandlers=[],
                 **kwargs):
        Agent.__init__(self,
                       name=name,
                       logHandlers=logHandlers)
        self.structure = structure
        
        # Data cache is a map from a parameter tag with an ExperimentResult
        # object
        self.data_cache = DataCache(name='data-cache',
                                    problems=problems,
                                    measures=measures)
        

        self.message_handlers['inform-measure-values'] = self.evaluate
        self.message_handlers['cfp-evaluate-parameter'] = \
                                                        self.create_cache_entry
        return

    def update_data_cache(self, paramTag, problem, measureValues):
        entry = self.data_cache.__getitem__(paramTag)
        entry.update_row(problem, measureValues)
        #log.debugger.log(str(entry.table))
        return
      
    
    
    # Message handlers
    def create_cache_entry(self, info):
        paramTag = info['proposition']['tag']
        parameterValues =  info['proposition']['parameter']
        self.data_cache.create_entry(paramTag, parameterValues)
        return

    
    def evaluate(self, info):
        # Update the cache
        
        paramTag = info['proposition']['parameter-tag']
        problem = info['proposition']['problem']
        measureValues = info['proposition']['values']
        #log.debugger.log('Update data cache by values: ' + str(measureValues))
        self.update_data_cache(paramTag, problem, measureValues)
        # Compute the model values
        parameters = self.data_cache.get_parameters(paramTag)
        storageRatio, measures = self.data_cache.get_measure_vectors(paramTag)
        #log.debugger.log('Add measure values of problem ' + problem # + \
        #                 #'and obtained measure vectors: ' + str(measures) +\
        #                 #' with storage ratio:' + str(storageRatio)
        #                 )
        objVal = self.structure.objective.evaluate(parameters, measures)
        if storageRatio < 1.0: # A partial data is obtained
            # Check if there is violation of objective function before
            # computing the constraint
            
            if self.structure.objective.is_partially_exceed(objVal):
                msg = Message(performative='inform',
                              sender=self.id,
                              content={'proposition':\
                                       {'what':'objective-exceeds',
                                        'parameter-tag':paramTag,
                                        'value':objVal
                                        }}
                              )
                self.send_message(msg)
                return
            # Evaluate the constraints
            consVals = []
            for cons in self.structure.constraints:
                val = cons.evaluate(parameters, measures)
                if cons.is_partially_violated(val):
                    msg = Message(performative='inform',
                             sender=self.id,
                             content={'proposition':\
                                       {'parameter-tag':paramTag,
                                        'what':'constraint-partially-violated',
                                        'who':cons.name,
                                        'value':consVals
                                       }}
                                  )
                    self.send_message(msg)
                    return
                consVals.append(val)
                # The message to inform partial model value is issued
            msg = Message(performative='inform',
                          sender=self.id,
                          content={'proposition':{'what':'partial-model-value',
                                                  'values':(objVal, consVals),
                                                  'parameter-tag':paramTag
                                                  }
                                   })
            self.send_message(msg)
            #log.debugger.log('Partial model with storage ratio ' + \
            #                 str(storageRatio) + ' is evaluated as ' + \
            #                 str(objVal) + ', ' + str(consVals))
            return
        # The full data is obtained, all of constraints are evaluated
        # without checking violation and update the bounds of objective function
        self.structure.objective.update_bounds(objVal)
        consVals = []
        for cons in self.structure.constraints:
            consVals.append(cons.evaluate(parameters, measures))
    
        msg = Message(performative='inform',
                          sender=self.id,
                          content={'proposition':{'what':'model-value',
                                                  'values':(objVal, consVals),
                                                  'parameter-tag':paramTag
                                                  }
                                   })
        self.send_message(msg)    
        return
    


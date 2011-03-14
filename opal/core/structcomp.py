import sys
import os.path
import marshal
import new
import log

from mafrw import Agent

class MeasureFunctionEvaluator(Agent):
    def __init__(self, 
                 name='measure function evaluator',
                 measureFunction=None,
                 logHandlers=[]):
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        return

class StructureComputer(Agent):
    """
    
    An object of this class represent for the model structure that is 
    described in Python language. The evaluator accept only ModelStructure 
    object as structure of model. Any structure modeled by other language 
    such as AMPL has to be rewritten as a ModelStructure object. This 
    can be done by the interpreters.
    """
    def __init__(self,
                 name='structcomp',
                 structure=None,
                 logHandlers=[],
                 **kwargs):
        Agent.__init__(self,
                       name=name,
                       logHandlers=logHandlers)
       
        self.structure = structure
        return

    def register(self, environment):
        
        Agent.register(self, environment)

        if self.structure is None:
            return

        objEval = MeasureFunctionEvaluator(name='objective',
                                           measureFunction=self.structure.objective)
        objEval.register(environment)

        if self.structure.constraints is None:
            return
        consIndex = 0
        for cons in self.structure.constraints:
            consEval = MeasureFunctionEvaluator(name='constraint ' + str(consIndex),
                                                measureFunction=cons.function)
            consEval.register(environment)
            consIndex = consIndex + 1
        return

    
    


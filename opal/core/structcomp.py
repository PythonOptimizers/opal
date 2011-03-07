import sys
import os.path
import marshal
import new
import log


from mafrw import Broker
from mafrw import Agent

class MeasureFunctionEvaluator(Agent):
    def __init__(self, 
                 name='measure function evaluator',
                 measureFunction=None,
                 logHandlers=[]):
        Agent.__init__(self, name=name, logHandlers=[])
        return

class StructureComputer(Broker):
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
        Broker.__init__(self,
                       name=name,
                       logHandlers=logHandlers)
        if structure is None:
            return

        objEval = MeasureFunctionEvaluator(name='objective',
                                           measureFunction=structure.objective,
                                           logHandlers=logHandlers)
        self.add_agent(objEval)

        if structure.constraints is not None:
            consIndex = 0
            for cons in structure.constraints:
                consEval = MeasureFunctionEvaluator(name='constraint ' + str(consIndex),
                                                    measureFunction=cons.function,
                                                    logHandlers=logHandlers)
                self.add_agent(consEval)
                consIndex = consIndex + 1
        return

    def handle_message(self, message):
        return

    def run(self):
        return

    


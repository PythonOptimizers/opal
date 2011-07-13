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

from .. import config



# =============================
class ModelData:
    """ 
    This class represents a data generator for a parameter optimization
    problem. The data is the values of the elementary measures that are needed
    to formulate the problem. To specify a data generator, we need provide:

    1. The algorithm 
    2. the set of elementary measures concerned 
    3. the set of parameters to control
    4. the test problems set.
    """

    def __init__(self, 
                 algorithm, 
                 problems=[],
                 parameters=None, 
                 measures=None,
                 **kwargs):
        # The core variables
        self.algorithm = algorithm
        if (problems is None) or (len(problems) == 0):
            self.problems = [TestProblem(name='TESTPROB')]
        else:
            self.problems = problems

        if parameters is None:
            self.parameters = algorithm.parameters
        else:
            self.parameters = parameters
        
        if measures is None:
            self.measures = algorithm.measures
        else:
            self.measures = measures

        self.running_options = {}
        self.running_options.update(kwargs)
        return

    def get_problems(self):
        return self.problems

    def get_algorithm(self):
        return self.algorithm

    def get_parameters(self):
        return self.parameters
    
    def get_measures(self):
        return self.measures
    
    def save(self, fileName):
        return

    def load(self, fileName):
        return


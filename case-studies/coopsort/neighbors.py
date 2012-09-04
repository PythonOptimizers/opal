import os
import sys
import string
import shutil
import pickle
import logging
from opal.Solvers.nomad import NOMADBlackbox
from opal.core.structureevaluator import FunctionEvaluator
worker = FunctionEvaluator(name="neighborhood-function evaluator", functionFile="neighbors.data")
# Create model evaluation environment
env = NOMADBlackbox(name="neighborhood blackbox", worker=worker, input=sys.argv[1], output=sys.stdout)
# Activate the environment
env.start()# Wait for environement finish his life time
env.join()

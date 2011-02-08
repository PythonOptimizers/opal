# Define a parameter optimization problem in relation to the 
# FD algorithm.
from fd_declaration import FD

from opal import OPALModelStructure
from opal import DataGenerator
from opal import OPALModel
from opal.Solvers import NOMAD

# Return the error measure.
def get_error(parameters, measures):
    val = sum(measures["ERROR"])
    return val

# Parameters being tuned and problem list.
params = FD.parameters   # All.
problems = []            # None.

# Define parameter optimization problem.
dataGen = DataGenerator(algorithmWrapper=FD, 
                        problems=problems, 
                        parameters=FD.parameters,
                        measures=FD.measures,
                        platform=SMP,
                        synchronization=True,
                        interruption=False)
struct = ModelStructure(objective=(get_error, False),  
                        constraints=[])  # Unconstrained
prob = OPALModel(dataSource=dataGen, 
                 modelStructure=struct)

# Solve parameter optimization problem.
NOMAD.solve(problem=prob)

# Inform user of expected optimal value for information.
try:
    import numpy as np
    eps = np.finfo(np.double).eps
except:
    # Approximate machine epsilon.
    eps = 1.0
    while 1+eps > 1: eps /= 2
    eps *= 2

from math import sqrt
print 'Expected optimal value is approximately %21.15e' % sqrt(eps)

# Define a parameter optimization problem in relation to the FD algorithm.
from fd_description import FD

from opal.core.testproblem import TestProblem
from opal import ModelStructure
from opal import ModelData
from opal import BlackBoxModel
from opal.Solvers import NOMAD

# Return the error measure.
def get_error(parameters, measures):
    val = measures["ERROR"].mean()
    return val

# Define a dummy test problem.
dummy = TestProblem(name='Dummy', description='Make believe')

# Parameters being tuned.
params = FD.parameters   # All.
problems = [dummy]

# Define parameter optimization problem.
data = ModelData(FD, [dummy], params) # FD.parameters['h'])
struct = ModelStructure(objective=get_error, constraints=[])  # Unconstrained
blackbox = BlackBoxModel(modelData=data, modelStructure=struct)

# Solve parameter optimization problem.
NOMAD.solve(model=blackbox)

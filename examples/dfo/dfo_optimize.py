# Simple demo: tune DFO parameters for CPU time on simple HS problems.
from opal import ModelStructure, ModelData, Model
from opal.TestProblemCollections import CUTEr
from dfo_declaration import DFO


from opal.Solvers import NOMAD

def avg_time(parameters,measures):
    n = len(measures['CPU']) 
    if n == 0:
        return 0.0
    return (sum(measures["CPU"]) + 0.0)/(n + 0.0)

# Select real parameters from DFO.
params = [par for par in DFO.parameters if par.is_real]

# Select tiny unconstrained HS problems.
problems = [prb for prb in CUTEr.HS if prb.nvar <= 5 and prb.ncon == 0]

print 'Working with parameters ', [par.name for par in params]
print 'Testing on problems ', [prb.name for prb in problems]

data = ModelData(DFO, problems, params)
structure = ModelStructure(objective=avg_time, constraints=[])  # Unconstrained

# Instantiate black-box solver.
model = Model(modelData=data, modelStructure=structure)

# Solve parameter optimization problem.
NOMAD.solve(blackbox=model)

# Simple demo: tune DFO parameters for CPU time on simple HS problems.
from dfo_declaration import DFO
from opal import ModelStructure, ModelData, Model
from opal.TestProblemCollections import CUTEr
from opal.Solvers import NOMAD

def avg_time(parameters,measures):
    return measures["CPU"].mean()

# Select real parameters from DFO.
params = [par for par in DFO.parameters if par.is_real]

# Select tiny unconstrained HS problems.
problems = [prb for prb in CUTEr.HS if prb.nvar <= 5 and prb.ncon == 0]

print 'Working with parameters ', [par.name for par in params]
print 'Testing on problems ', [prb.name for prb in problems]

data = ModelData(DFO, problems, params)
structure = ModelStructure(objective=avg_time)  # Unconstrained

# Instantiate black-box solver.
model = Model(modelData=data, modelStructure=structure)

# Solve parameter optimization problem.
NOMAD.set_parameter(name='DISPLAY_STATS',
                    value='%3dBBE [ %7.1eSOL, ]  %8.3eOBJ  %6.2fTIME')
NOMAD.solve(blackbox=model)

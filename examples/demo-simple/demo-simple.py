# Simple demo: tune DFO parameters for CPU time on simple HS problems.
from paropt.TestProblemCollections import CUTEr
from paropt.Algorithms import DFO
from paropt.Solvers import NOMAD
from paropt import ModelStructure
from paropt import ModelData
from paropt import BlackBox

def mu_time(p,measures):
    cpuTime = measures[0]
    return cpuTime(p).sum() / len(cpuTime(p))

# Select real parameters from DFO.
params = [par for par in DFO.parameters if par.is_real]

# Select tiny unconstrained HS problems.
problems = [prb for prb in CUTEr.HS if prb.nvar <= 5 and prb.ncon == 0]

print 'Working with parameters ', [par.name for par in params]
print 'Testing on problems ', [prb.name for prb in problems]

# Define parameter optimization problem.
structure = ModelStructure(objective=mu_time,constraints=[])  # Unconstrained
data = ModelData(DFO, problems, params)

# Instantiate black-box solver.
blackbox = BlackBox(modelData=data,modelStructure=structure)
 
NOMAD.set_parameter(name='MAX_BB_EVAL',value=2)

# Solve parameter optimization problem.
#blackbox.solve(solver=NOMAD)

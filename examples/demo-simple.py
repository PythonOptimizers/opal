# Simple demo: tune DFO parameters for CPU time on simple HS problems.

from paropt.TestProblemCollections import CUTEr
from paropt.Algorithms import DFO
from paropt.Solvers import NOMAD
from paropt.Measures import cpuTime #, funcEval, exitCode

from paropt import ModelStructure
from paropt import ModelData
from paropt import BlackBox

def mu_time(p):
    return cpuTime(p).sum() / len(cpuTime(p))

# Select algorithm
algorithm = DFO
    
# Select real parameters for DFO
params = [par for par in DFO.parameters if par.is_real]

# Select tiny unconstrained HS problems
problems = [prb for prb in CUTEr.HS if prb.nvar <= 5 and prb.ncon == 0]

# Select measure
measures = [cpuTime]


print 'Working with parameters ', [par.name for par in params]
print 'Testing on problems ', [prb.name for prb in problems]

# Define nonsmooth problem structure and data
model = ModelStructure(objective=avg_cpu_time)  # Unconstrained by default
data = ModelData(DFO, problems, params, [cpuTime])

# Define black box model and solve
blackbox = BlackBox(model,data)
#NOMAD.set_parameter(name='MAX_BB_EVAL',value=2)
blackbox.solve(solver=NOMAD)

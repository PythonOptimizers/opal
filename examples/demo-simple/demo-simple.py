# Simple demo: tune DFO parameters for CPU time on simple HS problems.
from opal.TestProblemCollections import CUTEr
from opal.Algorithms import DFO

from opal import ModelStructure
from opal import ModelData
from opal import BlackBoxModel
from opal import StatisticalMeasure

from opal.Solvers import NOMAD


#def avg_time(parameters,measures):
#    return measures["CPU"].mean()

# Select algorithm
algorithm = DFO
    
# Select real parameters for DFO
params = [par for par in DFO.parameters if par.is_real]

# Select tiny unconstrained HS problems
problems = [prb for prb in CUTEr.HS if prb.nvar <= 5 and prb.ncon == 0]

print 'Working with parameters ', [par.name for par in params]
print 'Testing on problems ', [prb.name for prb in problems]

data = ModelData(algorithm, problems, params)
structure = ModelStructure(objective=StatisticalMeasure.average('CPU'), constraints=[])  # Unconstrained

blackbox = BlackBoxModel(modelData=data,modelStructure=structure)
    
NOMAD.solve(model=blackbox)

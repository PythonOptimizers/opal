
from dev.paropt import TestProblem


from dev.paropt import ModelStructure
from dev.paropt import ModelData
from dev.paropt import BlackBox

from dev.paropt.Solvers import NOMAD

from gf_algorithm import GFCompAlg


problem = TestProblem(name='GF')
growth_factor_alg = GFCompAlg(matrixSize=4,initialMatrix='nomad-solution.higham-q4.txt')
growth_factor_alg.set_executable_command('/userdata/users/codan/local/python/bin/python gf_computing.py 1')
growth_factor_alg.set_parameter_file('matrix.txt')

def growth_factor(p,measures):
    growthFactor = measures[0]
    # We have only one test problem, so the first value of vector is itself
    return -growthFactor(p)[0]

    
# Select all parameter of algorithm
params = growth_factor_alg.parameters

# We have only "reprentative" test problem
problems = [problem]



print 'Working with parameters ', [par.name for par in params]
print 'Testing on problems ', [prb.name for prb in problems]

data = ModelData(growth_factor_alg, problems, params)
structure = ModelStructure(objective=growth_factor,constraints=[])  # Unconstrained

blackbox = BlackBox(modelData=data,modelStructure=structure)
    
NOMAD.set_parameter(name='MAX_BB_EVAL',value=50000)

blackbox.solve(solver=NOMAD)

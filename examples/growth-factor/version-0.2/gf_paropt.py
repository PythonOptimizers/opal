from dev.paropt import TestProblem
from dev.paropt import Algorithm
from dev.paropt import Parameter
from dev.paropt import Measure


from dev.paropt import ModelStructure
from dev.paropt import ModelData
from dev.paropt import BlackBox

from dev.paropt.Solvers import NOMAD

problem = TestProblem(name='GF')

matrix_size = 4
growth_factor_alg = Algorithm(name='GFC',purpose='Compute growth factor of a matrix')

for i in range(matrix_size*matrix_size):
    growth_factor_alg.add_param(Parameter(name='CELL'+str(i),kind='real',default=float(i+1)))
        
# Define the measures
growth_factor_alg.add_measure(Measure(name='GF',kind='real',description='Growth factor of Gaussian Elimination on the matrix'))
growth_factor_alg.set_executable_command('/userdata/users/codan/local/python/bin/python gf_computing.py 0')

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

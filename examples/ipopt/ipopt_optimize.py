from opal import ModelStructure, ModelData, Model, MeasureFunction
from ipopt_declaration import IPOPT

import sys

# Choose all parameters defined in declaration file
params = [param for param in IPOPT.parameters
          if param.name in ['tau_min', 's_theta', 's_phi', 'delta',
                             'max_soc', 'kappa_soc']]

# Choose all solvable problems 
#from ipopt_test_problems import ipopt_solvable_problems as problems
#from ipopt_test_problems import test_problems as problems
from ipopt_test_problems import CUTEr_constrained_problems

if len(sys.argv) > 1:
    f = open(sys.argv[1])
    representativeProblems = eval(f.read())
    f.close()

    problems = [ prob for prob in CUTEr_constrained_problems
                 if prob.name in representativeProblems ]
else:
    problems = CUTEr_constrained_problems
    
data = ModelData(IPOPT, problems, params)

from ipopt_composite_measures import sum_eval, sum_unsolvability
structure = ModelStructure(objective=MeasureFunction(sum_eval, addivity=1),
                           constraints=[(None, sum_unsolvability, 0)])

# Instantiate black-box solver.
from opal.Platforms import LSF
LSF.set_parameter({'MAX_TASK':10})

model = Model(modelData=data, modelStructure=structure, platform=LSF)

if len(sys.argv) > 2: # The initial point is provided by external file
    f = open(sys.argv[2])
    paramValues = eval(f.read())
    f.close()
    model.initial_points = [] # Reset the initial point set
    for tag in paramValues:
        model.add_initial_point(paramValues[tag])
    #print model.get_initial_points()

# Solve parameter optimization problem.
from opal.Solvers import NOMAD
#NOMAD.set_parameter(name='MAX_BB_EVAL', value=100)
#NOMAD.set_parameter(name='SCALING', value='scaling.txt')
NOMAD.set_parameter(name='INITIAL_MESH_SIZE',
                    value='(0.05 5 5 1 4 0.05)') 
#NOMAD.set_parameter(name='MIN_MESH_SIZE', value=1.0e-6)
NOMAD.set_parameter(name='MAX_MESH_INDEX', value=6)
NOMAD.set_parameter(name='DISPLAY_DEGREE', value=4)
NOMAD.solve(blackbox=model)

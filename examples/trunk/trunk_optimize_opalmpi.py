# Define a parameter optimization problem in relation to the TRUNK solver.
# This is a parallel version in which the test problems are solved in
# parallel. This parallelism is managed via MPI. This is an alternative to
# the parallelization implemented in trunk_optimize_lsf.py.
from trunk_declaration import trunk

from opal import ModelStructure
from opal import ModelData
from opal import BlackBoxModel
from opal.Solvers import NOMAD

from opal.TestProblemCollections import CUTEr
from opal.Platforms import OPALMPI

def get_error(parameters, measures):
    val = sum(measures["FEVAL"])
    return val

# Parameters being tuned and problem list.
par_names = ['eta1', 'eta2', 'gamma1', 'gamma2', 'gamma3']
params = [param for param in trunk.parameters if param.name in par_names]

problems = [problem for problem in CUTEr if problem.name in ['BDQRTIC',
                                                             'BROYDN7D',
                                                             'BRYBND',
                                                             'CURLY10',
                                                             'CURLY20',
                                                             'CURLY30',
                                                             'CRAGGLVY',
                                                             'DIXON3DQ',
                                                             'EIGENALS',
                                                             'FMINSRF2',
                                                             'FMINSURF',
                                                             'GENROSE',
                                                             'HIELOW',
                                                             'MANCINO',
                                                             'NCB20',
                                                             'NCB20B',
                                                             'NONDQUAR',
                                                             'POWER',
                                                             'SENSORS',
                                                             'SINQUAD',
                                                             'TESTQUAD',
                                                             'TRIDIA',
                                                             'WOODS']]


# Define parameter optimization problem.

data = ModelData(algorithm=trunk,
                 problems=problems,
                 activeParameters=params,
                 platform=OPALMPI)
struct = ModelStructure(objective=get_error,
                        constraints=[])  # Unconstrained
blackbox = BlackBoxModel(modelData=data, modelStructure=struct)

# Solve parameter optimization problem.
NOMAD.set_parameter(name='MAX_BB_EVAL', value=500)
NOMAD.solve(model=blackbox)

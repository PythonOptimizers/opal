# Define a parameter optimization problem in relation to the TRUNK solver.
# This is a parallel version in which the test problems are solved in
# parallel in independent subprocesses. This strategy effectively
# parallelizes the black box. This is an alternative to the parallelization
# implemented in trunk_optimize_opalmpi.py.
from trunk_declaration import trunk
from opal import ModelStructure, ModelData, Model
from opal.Solvers import NOMADMPI
from opal.TestProblemCollections import CUTEr
from opal.Platforms import SMP

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
                 parameters=params)
struct = ModelStructure(objective=get_error,
                        constraints=[])  # Unconstrained
model = Model(modelData=data, modelStructure=struct, platform=SMP)

# Solve parameter optimization problem.
NOMADMPI.set_mpi_config(name='np', value=5)
NOMADMPI.set_parameter(name='MAX_BB_EVAL', value=5)
NOMADMPI.set_parameter(name='DISPLAY_DEGREE', value=2)
NOMADMPI.solve(blackbox=model)

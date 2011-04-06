# Define a parameter optimization problem in relation to the TRUNK solver.
# This is a parallel version in which the black box solver evaluates the
# worth of neighbors in parallel. The black box evaluation itself is
# sequential.
from trunk_declaration import trunk
from opal import ModelStructure, ModelData, Model
from opal.Solvers import NOMADMPI

from opal.TestProblemCollections import CUTEr


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
blackbox = Model(modelData=data, modelStructure=struct)

# Solve parameter optimization problem.
NOMADMPI.set_mpi_config(name='np', value=8)
NOMADMPI.set_mpi_config(name='-host', value='lin01,lin02,lin03,lin04')
NOMADMPI.set_parameter(name='MAX_BB_EVAL', value=50)
NOMADMPI.set_parameter(name='DISPLAY_DEGREE', value=2)
NOMADMPI.solve(model=blackbox)

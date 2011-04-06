# Define a parameter optimization problem in relation to the TRUNK solver.
# This is a parallel version in which the test problems are placed in a
# LSF queue to be solved in parallel. This strategy effectively
# parallelizes the black box. This is an alternative to the parallelization
# implemented in trunk_optimize_opalmpi.py.
from trunk_declaration import trunk
from opal import ModelStructure, ModelData, Model
from opal.Solvers import NOMAD

from opal.TestProblemCollections import CUTEr
from opal.Platforms import LSF

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
                                                             'NONDQUAR',
                                                             'POWER',
                                                             'SENSORS',
                                                             'SINQUAD',
                                                             'TESTQUAD',
                                                             'TRIDIA',
                                                             'WOODS']]

# Define parameter optimization problem.
LSF.set_config(parameterName="-m",
               parameterValue='"lin01 lin02 lin03 lin04"')
LSF.set_config(parameterName="-q",
               parameterValue="fedora")
data = ModelData(algorithm=trunk,
                 problems=problems,
                 activeParameters=params,
                 platform=LSF)
struct = ModelStructure(objective=get_error,
                        constraints=[])  # Unconstrained
blackbox = Model(modelData=data, modelStructure=struct)

# Solve parameter optimization problem.
NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
NOMAD.solve(model=blackbox)

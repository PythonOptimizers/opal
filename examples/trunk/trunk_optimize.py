# Define a parameter optimization problem in relation to the TRUNK solver.
from trunk_declaration import trunk

from opal import OPALModelStructure
from opal import DataGenerator
from opal import OPALModel
from opal.Solvers import NOMAD

from opal.TestProblemCollections import CUTEr

def get_error(parameters, measures):
    val = sum(measures["ECODE"])
    return val

def sum_heval(parameters, measures):
    val = sum(measures['ECODE'])
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

SMP.set_parameter(name='MAX_PROC', value=5);

# Define parameter optimization problem.
dataGen = DataGenerator(algorithmWrapper=trunk,
                        problems=problems,
                        parameters=params,
                        platform=SMP,
                        synchronization=False,
                        interruption=True)

struct = ModelStructure(objective=(sum_heval, True)
                        constraints=[(None, get_error, 0, True)])  # Unconstrained
prob = OPALModel(dataSource=dataGen, 
                 modelStructure=struct)

# Solve parameter optimization problem.
NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
NOMAD.solve(problem=prob)

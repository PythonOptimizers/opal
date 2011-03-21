# Define a parameter optimization problem in relation to the TRUNK solver.
# This is the sequential version.
from trunk_declaration import trunk

from opal import ModelStructure
from opal import ModelData
from opal import BlackBoxModel
from opal.Solvers import NOMAD

from opal.TestProblemCollections import CUTEr
def sum_heval(parameters, measures):
    val = sum(measures['HEVAL'])
    return val

def get_error(parameters, measures):
    val = sum(measures["ECODE"])
    return val

# Parameters being tuned and problem list.
par_names = ['eta1', 'eta2', 'gamma1', 'gamma2', 'gamma3']
#params = [param for param in trunk.parameters if param.name in par_names]

params = [trunk.parameters['eta1'],
	  trunk.parameters['eta2']]
problems = [problem for problem in CUTEr if problem.name in ['BDQRTIC',
                                                             'BROYDN7D',
                                                             'BRYBND',
#                                                             'CURLY10',
#                                                             'CURLY20',
#                                                             'CURLY30',
#                                                             'CRAGGLVY',
#                                                             'DIXON3DQ',
#                                                             'EIGENALS',
#                                                             'FMINSRF2',
#                                                             'FMINSURF',
#                                                             'GENROSE',
                                                             'HIELOW',
#                                                             'MANCINO',
#                                                             'NCB20',
#                                                             'NCB20B',
#                                                             'NONDQUAR',
#                                                             'POWER',
#                                                             'SENSORS',
#                                                             'SINQUAD',
                                                             'TESTQUAD',
                                                             'TRIDIA',
                                                             'WOODS']]

# Define parameter optimization problem.
data = ModelData(algorithm=trunk,
                 problems=problems,
                 activeParameters=params)
struct = ModelStructure(objective=sum_heval,
                        constraints=[(None, get_error, 0)])
blackbox = BlackBoxModel(modelData=data, modelStructure=struct)

# Solve parameter optimization problem.
NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
NOMAD.solve(model=blackbox)

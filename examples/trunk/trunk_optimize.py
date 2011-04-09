# Define a parameter optimization problem in relation to the TRUNK solver.
from trunk_declaration import trunk

from opal import ModelStructure, ModelData, Model, MeasureFunction
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

params = [trunk.parameters['eta1'], trunk.parameters['eta2']]
problems = [problem for problem in CUTEr if problem.name in ['BDQRTIC',
#                                                             'BROYDN7D',
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

#SMP.set_parameter(name='MAX_PROC', value=5);

# Define parameter optimization problem.
data = ModelData(algorithm=trunk,
                 problems=problems,
                 parameters=params,
                 measures=trunk.measures)

struct = ModelStructure(objective=MeasureFunction(sum_heval,
                                                  additivity=1),
                        constraints=[(None,
                                      MeasureFunction(get_error, addivity=1),
                                      0)])  # One constraint get_error(p) <= 0


prob = Model(modelData=data, 
             modelStructure=struct,
             platform='SMP',
             synchoronized=False,
             interruptible=True
             )

# Solve parameter optimization problem.

if __name__ == '__main__':
    from opal.Solvers import NOMAD
    NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
    NOMAD.solve(model=prob)


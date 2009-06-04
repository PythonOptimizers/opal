import sys

from paropt.TestProblemCollections import CUTEr
from paropt.Algorithms import DFO
from paropt.Measures import cpuTime, funcEval, exitCode, funcVal
from paropt.Solvers import NOMAD
from paropt.Platforms import LSF

from paropt import ModelData
from paropt import ModelStructure

from model import solving_percent,sum_of_func_eval,mean_of_cpu_time,p2,probNames,measureValues,quality_asset

problemSet = 'hse'
probList = [prob for prob in CUTEr.HS if prob.name in probNames[problemSet]]

#probList = [prob for prob in CUTEr.extract(nMax=100,mMax=0) if prob.name in probNames[problemSet]]

optimizedParams = [param for param in DFO.parameters if param.name in ['DELMIN','STPTHR','DELTA','CNSTOL','PP']]

measures = [cpuTime, funcEval,exitCode,funcVal]

optModel = ModelStructure(objective=p2,
                          constraints=[(mean_of_cpu_time,
                                        measureValues[problemSet][0]),
                                       (sum_of_func_eval,
                                        measureValues[problemSet][1]),
                                       solving_percent,
                                       (quality_asset,1.0)])

optData = ModelData(DFO, probList, optimizedParams, measures, platform=LSF)

blackbox = NOMAD.BlackBox(optData,optModel)
blackbox.set_parameter(NOMAD.Parameter('LOWER_BOUND','(1e-8 1e-16 0 1e-8 1)'))
blackbox.set_parameter(NOMAD.Parameter('UPPER_BOUND','(1e-3 1e-3 0.1 - -)'))
blackbox.set_parameter(NOMAD.Parameter('INITIAL_MESH_SIZE','(1e-5 1e-5 0.01 0.1 1)'))

blackbox.solve()


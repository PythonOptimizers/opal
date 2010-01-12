import sys

# Simple demo: tune DFO parameters for CPU time on simple HS problems.
from dev.opal.TestProblemCollections import CUTEr
from dev.opal.TestProblemCollections import CUTErQuery
from dev.opal.Algorithms import DFO
from dev.opal.Solvers import NOMAD
from dev.opal.Platforms import LSF
from dev.opal.Platforms import LINUX

from dev.opal import ModelStructure
from dev.opal import ModelData
from dev.opal import BlackBox
from dev.opal.core.measure import Measure

DFO.set_executable_command('python dfo_minimizer_2.py')
DFO.add_measure(Measure(kind='real',name='DESCENT',description='Descent of function value = f^0 - f^*'))
[param for param in DFO.parameters if param.name == 'PP'][0].set_default(1000)
#LSF.set_config('-q','suse')

# The model functions are built from two components
# The parameter vector and the measure matrix (table)
def unsolved_percent(parameters,measures):
    solved = measures['EXITCODE']
    nProb = len(solved) + 0.0
    unsolvedProb = 0.0
    for i in range(len(solved)):
        if solved[i] != 0:
            unsolvedProb = unsolvedProb + 1.0
    return float(unsolvedProb/nProb)

def sum_of_cpu_time_ratio(parameters,measures):
    cpuTime = measures['CPU']
    #print 'dfoparam',measures['FVAL']
    #nProb = len(cpuTime)
    import data
    defaultCpuTime = data.get_default_cpu_time(measures.get_problems())
    ratio = (cpuTime - defaultCpuTime)/(defaultCpuTime + cpuTime)
    return ratio.sum()

def sum_of_func_eval_ratio(parameters,measures):
    funcEval = measures['FEVAL']
    #print 'dfoparam',measures['FVAL']
    #nProb = len(cpuTime)
    import data
    defaultFuncEval = data.get_default_func_eval(measures.get_problems())
    ratio = (funcEval-defaultFuncEval)/(defaultFuncEval + funcEval)
    return ratio.sum()

def quality_asset(parameters,measures):
    finalValue = measures['FVAL']
    #print 'dfoparam',finalValue
    nProb = len(finalValue)
    worseSolution = 0.0
    import data
    defaultFinalValue = data.get_default_final_values(measures.get_problems())
    distance = finalValue - defaultFinalValue
    #print defaultFinalValue,finalValue,distance
    #print measures.get_problems(),finalValue, defaultFinalValue,distance
    for i in range(len(distance)):
        if distance[i] > 0.001:
            worseSolution = worseSolution + 1.0
    return worseSolution/nProb

def test_func(parameters,measures):
    return 1

uncons = [prob for prob in CUTEr.select(CUTErQuery(constraintType='U')) 
          if prob.nvar <=50]

#longProb = ['CHNROSNB','ERRINROS','TOINTPSP','VAREIGVL']

longProb = ['BARD','CKOEHELB','CHNROSNB','ERRINROS','TOINTPSP','TOINTGOR','TOINTQOR','VAREIGVL','SCHMVETT']

#print '[dfoparam.py]',
testProb = [prob for prob in uncons if prob.name in ['HEART6LS','KOWOSB','OSBORNEB']]
unconsSamples = []
consSamples = []

problemSets = {'uncons':unconsSamples,
               'cons':consSamples}

if len(sys.argv) < 3:
    nFold = 2
else:
    nFold = int(sys.argv[2])

if len(sys.argv) < 2:
    setName = 'cons'
else:
    setName = sys.argv[1]

i = 1
for prob in uncons:
    if prob.name in longProb:
        continue
    if i % nFold == 0:
        unconsSamples.append(prob)
    i = i + 1

i = 1

for prob in CUTEr.HS:
    if prob.name in ["HS99EXP"]:
        continue
    if (i % nFold == 0):
        consSamples.append(prob)
    i = i + 1

# There is no problem HS58, HS82, HS94, HS115, HS99
# Problem HS99EXP replaces for HS99 but it has so many constraint: 
# 31 constraints, we have to allocate an array of 93 = 31*3
# Even the dfo.f90 does not work

#print '[dfoparam.py]',[prob.name for prob in problems]
params = [param for param in DFO.parameters if param.name in ['DELMIN','DELTA','PP']]
data = ModelData(DFO, problemSets[setName], params,platform=LSF)

structure = ModelStructure(objective=sum_of_func_eval_ratio,
                           constraints=[(unsolved_percent,0),
                                        (quality_asset,0.2)
                                        ]
                           )

blackbox = BlackBox(modelData=data,modelStructure=structure,
                    logFileName=setName + '-1-' + str(nFold - 1) + '.log')
#surrogate = blackbox.generate_surrogate()
   
NOMAD.set_parameter(name='MAX_BB_EVAL',value=300)
NOMAD.set_parameter(name='INITIAL_MESH_SIZE',value='(1e-5 1 10)')


blackbox.solve(solver=NOMAD) #,
              # surrogate=surrogate)



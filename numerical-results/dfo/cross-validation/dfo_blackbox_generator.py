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
from dev.opal.core.log import PythonLogging

DFO.set_executable_command('python dfo_minimizer_2.py')
[param for param in DFO.parameters if param.name == 'PP'][0].set_default(1000)
DFO.add_measure(Measure(kind='real',name='DESCENT',description='Descent of function value = f^0 - f^*'))


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

def mean_of_cpu_time(parameters,measures):
    cpuTime = measures['CPU']
    #print 'dfoparam',measures['FVAL']
    nProb = len(cpuTime)
    return cpuTime.sum()/nProb

def sum_of_func_eval(parameters,measures):
    funcEval = measures['FEVAL']
    #print 'dfoparam',measures['FVAL']
    #nProb = len(cpuTime)
    return funcEval.sum()

def sum_of_cpu_time_ratio(parameters,measures):
    cpuTime = measures['CPU']
    #print 'dfoparam',measures['FVAL']
    #nProb = len(cpuTime)
    import data
    defaultCpuTime = data.get_default_cpu_time(measures.get_problems())
    ratio = (cpuTime - defaultCpuTime)/defaultCpuTime
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
    stpthr = parameters['STPTHR'].value
    #print 'dfoparam',finalValue
    nProb = len(finalValue)
    worseSolution = 0.0
    import data
    defaultFinalValue = data.get_default_final_values(measures.get_problems())
    distance = finalValue - defaultFinalValue
    #print defaultFinalValue,finalValue,distance
    #print measures.get_problems(),finalValue, defaultFinalValue,distance
    for i in range(len(distance)):
        if distance[i] > stpthr:
            worseSolution = worseSolution + 1.0
    return worseSolution/nProb

def test_func(parameters,measures):
    return 0

uncons = [prob for prob in CUTEr.select(CUTErQuery(constraintType='U')) 
          if prob.nvar <=50]


#longProb = ['BARD','CKOEHELB','CHNROSNB','ERRINROS','TOINTPSP','TOINTGOR','TOINTQOR','VAREIGVL','SCHMVETT',
#            'CURLY30','SCURLY30', 'PARKCH' 
#            ]
longProb = ['BARD','CKOEHELB','CHNROSNB','ERRINROS','TOINTPSP','TOINTGOR','TOINTQOR','VAREIGVL','SCHMVETT']
# CKOEHELB is not in the database 
# SCHMVETT has NaN final value
# SCURLY30 *** Warning message from routine MA57BD **   INFO(1) = 4
#     Matrix is singular, rank =    8
# PARKCH    
#  ** Exit from MAKEFN - insufficient space. Increase size of NSETVC
#     Return from MAKEFN, INFORM = -12


#print '[dfoparam.py]',
#testProb = [prob for prob in uncons if prob.name in ['HEART6LS','KOWOSB','OSBORNEB']]
all = []
test_uncons = []
cross_uncons = []
all_uncons = []

if len(sys.argv) < 3:
    nFold = 2
else:
    nFold = int(sys.argv[2])
i = 1
for prob in uncons:
    if prob.name in longProb:
        continue
    if (i % nFold == 0) :
        test_uncons.append(prob)
    else:
        cross_uncons.append(prob)
    all.append(prob)
    all_uncons.append(prob)
    i = i + 1


test_cons = []
cross_cons = []
all_cons = []
i = 1
for prob in CUTEr.HS:
    if prob.name in ['HS99EXP']:
        continue
    if (i % nFold == 0) :
        test_cons.append(prob)
    else:
        cross_cons.append(prob)
    all.append(prob)
    all_cons.append(prob)
    i = i + 1

test = [prob for prob in all if prob.name in ['AKAVIA','BIGGS6','HS10','HS54']]
setName = sys.argv[1]

problems = {'cross_cons':cross_cons,
            'cross_uncons':cross_uncons,
            'test_cons':test_cons,
            'test_uncons':test_uncons,
            'all_cons':all_cons,
            'all_uncons':all_uncons,
            'all':all,
            'test':test}

#print '[dfoparam.py]',[prob.name for prob in problems]
params = [param for param in DFO.parameters if param.name in ['DELMIN','STPTHR','CNSTOL','DELTA','PP']]
data = ModelData(DFO, problems[setName], params,platform=LSF)#, logging=PythonLogging())


structure = ModelStructure(objective=test_func,
                           constraints=[]
                           )

blackbox = BlackBox(modelData=data,modelStructure=structure,
                    runFileName=setName + '_bb-1-' + str(nFold - 1) + '.py',
                    dataFileName=setName + '_bb-1-' + str(nFold - 1) + '.dat',
                    logFileName=setName + '-1-' + str(nFold - 1) + '.log')
blackbox.generate_executable_file()
blackbox.save()




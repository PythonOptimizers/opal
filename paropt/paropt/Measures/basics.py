from ..core.measure import *

cpuTime = Measure(name='STIME',
                  kind='real',
                  description='CPU usage time')

funcEval = Measure(name='NFEVAL',
                   kind='integer',
                   description='Number of function evalution')

iterNum = Measure(name='NITER',
                  kind='integer',
                  description='Number of iteration')

funcVal = Measure(name='FVAL',
                  kind='real',
                  description='Objective function value')

exitCode = Measure(name='EXITCODE',
                   kind='integer',
                   description='Exit code')

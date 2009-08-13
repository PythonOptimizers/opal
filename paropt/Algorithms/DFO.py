from ..core.parameter import *
from ..core.measure import Measure
from ..core.algorithm import Algorithm

# Define new algorithm 
DFO = Algorithm(name='DFO', purpose='Derivative-free Optimization')

# Register executable for DFO
DFO.set_executable_command('python dfo_minimizer.py')

# Register parameter file
DFO.set_parameter_file('dfo.param')

# Define parameters
nx = Parameter(kind='integer', default=1, name='NX')
maxit = Parameter(kind='integer', default=5000, name='MAXIT')
maxef = Parameter(kind='integer', default=9500, name='MAXNF')
stpcrtr = Parameter(kind='integer', default=2, name='STPCRTR')
delmin = Parameter(default=1.0e-3, name='DELMIN',bound=(1.0e-8,1.0e-3))
stpthr = Parameter(default=1.0e-3, name='STPTHR',bound=(0,None))
cnstol = Parameter(default=1.0e-5, name='CNSTOL',bound=(0,0.1))
delta = Parameter(default=1.0e0, name='DELTA',bound=(1.0e-8,None))
pp = Parameter(default=1.0e0, name='PP',bound=(1,None))
scale = Parameter(kind='integer', default=0, name='SCALE')
iprint = Parameter(kind='integer', default=1, name='IPRINT')

# Register parameters with algorithm
DFO.add_param(nx)
DFO.add_param(maxit)
DFO.add_param(maxef)
DFO.add_param(stpcrtr)
DFO.add_param(delmin)
DFO.add_param(stpthr)
DFO.add_param(cnstol)
DFO.add_param(delta)
DFO.add_param(pp)
DFO.add_param(scale)
DFO.add_param(iprint)

# Define the feasible region
#DFO.add_parameter_constraint('DELMIN >= 1.0e-8')
#DFO.add_parameter_constraint('DELMIN <= 1.0e-3')
#DFO.add_parameter_constraint('STPTHR >= 0')
#DFO.add_parameter_constraint('STPTHR <= 1.0e-3')
#DFO.add_parameter_constraint('CNSTOL >= 0')
#DFO.add_parameter_constraint('CNSTOL <= 0.1')
DFO.add_parameter_constraint('DELTA >= DELMIN')
#DFO.add_parameter_constraint('PP >= 1')

# Define and register the measures
DFO.add_measure(Measure(kind='integer',name='EXITCODE',description='Exit code'))
DFO.add_measure(Measure(kind="real",name='FVAL',description='Function value'))
DFO.add_measure(Measure(kind='real',name='CPU',description='CPU time usage'))
DFO.add_measure(Measure(kind='real',name='FEVAL',description='Number of function evaluations'))



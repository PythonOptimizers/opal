from ..core.parameter import *
from ..core.algorithm import Algorithm

# Define new algorithm 
DFO = Algorithm(name='DFO', purpose='Derivative-free Optimization')
# Define the executing 

DFO.set_executable('python dfo_minimizer.py')

DFO.set_parameter_file('dfo.param')

# Define parameters
nx = Parameter(kind='integer', default=1, name='NX')
maxit = Parameter(kind='integer', default=5000, name='MAXIT')
maxef = Parameter(kind='integer', default=9500, name='MAXEF')
stpcrtr = Parameter(kind='integer', default=2, name='STPCRTR')
delmin = Parameter(default=1.0e-3, name='DELMIN')
stpthr = Parameter(default=1.0e-3, name='STPTHR')
cnstol = Parameter(default=1.0e-5, name='CNSTOL')
delta = Parameter(default=1.0e0, name='DELTA')
pp = Parameter(default=1.0e0, name='PP')
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
DFO.add_parameter_constraint('DELMIN >= 1.0e-8')
DFO.add_parameter_constraint('DELMIN <= 1.0e-3')
DFO.add_parameter_constraint('STPTHR >= 0')
#DFO.add_parameter_constraint('STPTHR <= 1.0e-3')
DFO.add_parameter_constraint('CNSTOL >= 0')
DFO.add_parameter_constraint('CNSTOL <= 0.1')
DFO.add_parameter_constraint('DELTA >= DELMIN')
DFO.add_parameter_constraint('PP >= 1')




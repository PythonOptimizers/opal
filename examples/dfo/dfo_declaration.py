from opal.core.algorithm import Algorithm
from opal.core.parameter import Parameter
from opal.core.measure   import Measure

# Define new algorithm.
DFO = Algorithm(name='DFO', description='Derivative-free Optimization')

# Register executable for DFO.
DFO.set_executable_command('python dfo_run.py')

# Register parameter file.
DFO.set_parameter_file('dfo.param')

# Define parameters.
nx = Parameter(kind='integer', default=1, name='NX')
maxit = Parameter(kind='integer', default=5000, name='MAXIT')
maxef = Parameter(kind='integer', default=9500, name='MAXNF')
stpcrtr = Parameter(kind='integer', default=2, name='STPCRTR')
delmin = Parameter(default=1.0e-4, name='DELMIN',bound=(1.0e-8,1.0e-3))
stpthr = Parameter(default=1.0e-3, name='STPTHR',bound=(0,None))
cnstol = Parameter(default=1.0e-5, name='CNSTOL',bound=(0,0.1))
delta = Parameter(default=1.0e0, name='DELTA',bound=(1.0e-8,None))
pp = Parameter(default=1.0e0, name='PP',bound=(1,None))
scale = Parameter(kind='integer', default=0, name='SCALE')
iprint = Parameter(kind='integer', default=1, name='IPRINT')

# Register parameters with algorithm.
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

# Define the feasible region.
DFO.add_parameter_constraint('DELTA >= DELMIN')

# Define and register measures.
exitcode = Measure(kind='integer', name='EXITCODE', description='Exit code')
fval = Measure(kind='real', name='FVAL', description='Function value')
cpu = Measure(kind='real', name='CPU', description='CPU time usage')
feval = Measure(kind='real', name='FEVAL',
                description='Number of function evaluations')

DFO.add_measure(exitcode)
DFO.add_measure(fval)
DFO.add_measure(cpu)
DFO.add_measure(feval)

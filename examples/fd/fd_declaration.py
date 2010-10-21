# Description of the foward finite-difference "algorithm".
from opal.core.algorithm import Algorithm
from opal.core.parameter import Parameter
from opal.core.measure   import Measure

# Define Algorithm object.
FD = Algorithm(name='FD', purpose='Forward Finite Differences')

# Register executable for FD.
FD.set_executable_command('python fd_run.py')

# Register parameter file used by black-box solver to communicate with FD.
#FD.set_parameter_file('fd.param')  # Should be chosen automatically and hidden.

# Define parameter and register it with algorithm.
h = Parameter(kind='real', default=0.5, bound=(0, None),
              name='h', description='Step size')
FD.add_param(h)

# Define relevant measure and register with algorithm.
error = Measure(kind='real', name='ERROR', description='Error in derivative')
FD.add_measure(error)

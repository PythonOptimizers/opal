from opal.core.algorithm import Algorithm
from opal.core.parameter import Parameter
from opal.core.measure import Measure

# Define new algorithm.
coopsort = Algorithm(name='CoopSort', description='Sort Algorithm')

# Register executable for .
coopsort.set_executable_command('python coopsort_run.py')

# Define parameters.

# 5. Line search parameters
coopsort.add_param(Parameter(name='coopTree',
                             kind='categorical',
                             default=0,
                             description='An encoded number represents cooperation tree'))

coopsort.add_measure(Measure(name='TIME',
                             kind='real',
                             description='Computing time'))

from opal.core.algorithm import Algorithm
from opal.core.parameter import Parameter
from opal.core.measure import Measure

# Define new algorithm.
coopsort = Algorithm(name='CoopSort', description='Sort Algorithm')

# Register executable.
coopsort.set_executable_command('python coopsort_run.py')

# Define parameters.

# The following coop tree amounts to 5522522 (in base 6.)
coopsort.add_param(Parameter(name='coopTree',
                             kind='categorical',
                             default=275378,
                             #default=284354431,
                             description='Encoded cooperation tree'))

# This dummy parameter is just there to circumvent a bug in NOMAD
# that occurs when the problem has a single parameter and this parameter
# is categorical.
coopsort.add_param(Parameter(name='nothing',
                             kind='integer',
                             default=0,
                             description='To avoid a bug in NOMAD'))

coopsort.add_measure(Measure(name='TIME',
                             kind='real',
                             description='Computing time'))

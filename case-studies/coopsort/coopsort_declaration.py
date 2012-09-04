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
                             #default=4422422,
                             #default=5511511,
                             #default=444224224422422,
                             #default=375297539054, # 444224224422422 in base 6
                             #default=220910, # 4422422 in base 6
                             #default=374872314751 # 444114114411411
                             #default=2813455869998, #555225225522522
                             default=356913842, #55225522522
                             #default=2,
                             #default=275378, #5522522
                             #default=219391, #4411411
                             description='An encoded number represents cooperation tree'))

coopsort.add_param(Parameter(name='nothing',
                             kind='integer',
                             default=0,
                             description='For avoiding the bug of one categorical variable of NOMAD'))
			    
coopsort.add_measure(Measure(name='TIME',
                             kind='real',
                             description='Computing time'))

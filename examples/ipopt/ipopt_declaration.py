from opal.core.algorithm import Algorithm
from opal.core.parameter import Parameter
from opal.core.measure import Measure

# Define new algorithm.
IPOPT = Algorithm(name='IPOPT', description='Interior Point for OPTimization')

# Register executable for IPOPT.
IPOPT.set_executable_command('python ipopt_run.py')

# Define parameters.

# 5. Line search parameters
IPOPT.add_param(Parameter(name='tau_min',
                          kind='real',
                          bound=[0, 1],
                          default=0.99,
                          description='For fraction-to-boundary rule'))
IPOPT.add_param(Parameter(name='s_theta',
                          kind='real',
                          bound=[0, None],
                          default=1.1,
                          description='Exponent for current constraint ' +\
                          'violation'))
IPOPT.add_param(Parameter(name='s_phi',
                          kind='real',
                          bound=[0, None],
                          default=2.3,
                          description='Exponent for linear barrier function ' +\
                          'model'))
IPOPT.add_param(Parameter(name='delta',
                          kind='real',
                          bound=[0, None],
                          default=1.0,
                          description='Multiplier for constraint violation'))
IPOPT.add_param(Parameter(name='eta_phi',
                          kind='real',
                          bound=[0, None],
                          default=1.0e-8,
                          description='Multiplier for constraint violation'))
IPOPT.add_param(Parameter(name='theta_min_fact',
                          kind='real',
                          bound=[0, None],
                          default=1.0e-4,
                          description='Factor for constraint violation ' +\
                          'threshod'))
IPOPT.add_param(Parameter(name='theta_max_fact',
                          kind='real',
                          bound=[0, None],
                          default=1.0e4,
                          description='Factor of upper bound for constraint '+\
                          'violation'))
IPOPT.add_param(Parameter(name='gamma_theta',
                          kind='real',
                          bound=[0, 1],
                          default=1.0e-8,
                          description='Relaxation factor in the filter ' +\
                          'margin for the constraint violation'))
IPOPT.add_param(Parameter(name='gamma_phi',
                          kind='real',
                          bound=[0, 1],
                          default=1.0e-8,
                          description='Relaxation factor in the filter ' +\
                          'margin for barrier function'))
IPOPT.add_param(Parameter(name='max_soc',
                          kind='integer',
                          bound=[0, None],
                          default=4,
                          description='Maximum number of iteration for ' +\
                          'second order correction'))
IPOPT.add_param(Parameter(name='kappa_soc',
                          kind='real',
                          bound=[0, 1],
                          default=0.99,
                          description='Maximum number of iteration for ' +\
                          'second order correction'))

# Define the feasible region.
IPOPT.add_parameter_constraint('tau_min > 0')
IPOPT.add_parameter_constraint('tau_min < 1')
IPOPT.add_parameter_constraint('s_theta > 1')
IPOPT.add_parameter_constraint('s_phi > 1')
IPOPT.add_parameter_constraint('delta > 0')
IPOPT.add_parameter_constraint('eta_phi > 0')
IPOPT.add_parameter_constraint('eta_phi < 0.5')
IPOPT.add_parameter_constraint('theta_min_fact > 0')
IPOPT.add_parameter_constraint('theta_max_fact > 0')
IPOPT.add_parameter_constraint('gamma_theta > 0')
IPOPT.add_parameter_constraint('gamma_theta < 1')
IPOPT.add_parameter_constraint('gamma_phi > 0')
IPOPT.add_parameter_constraint('gamma_phi < 1')
IPOPT.add_parameter_constraint('kappa_soc > 0')
IPOPT.add_parameter_constraint('kappa_soc < 1')
# Define and register measures.
IPOPT.add_measure(Measure(name='CPU',
                          kind='real',
                          description='Computing time'))
IPOPT.add_measure(Measure(name='FEVAL',
                          kind='integer',
                          description='Number of evaluation of objective function'))
IPOPT.add_measure(Measure(name='EQCVAL',
                          kind='integer',
                          description='Number of evaluation of equality constraints'))
IPOPT.add_measure(Measure(name='INCVAL',
                          kind='integer',
                          description='Number of evaluation of inequality constraints'))
IPOPT.add_measure(Measure(name='GEVAL',
                          kind='integer',
                          description='Number of evaluation of function objective gradient'))
IPOPT.add_measure(Measure(name='EQJVAL',
                          kind='integer',
                          description='Number of evaluation of equality constraint jacobian matrix'))
IPOPT.add_measure(Measure(name='INJVAL',
                          kind='integer',
                          description='Number of evaluation of inequatily constraint jacobian matrix'))
IPOPT.add_measure(Measure(name='ECODE',
                          kind='integer',
                          description='Exit code'))

IPOPT.add_measure(Measure(name='NITER',
                          kind='integer',
                          description='Number of iteration'))

IPOPT.add_measure(Measure(name='WEIGHT',
                          kind='real',
                          description='weight for a measure vector of a problem'))

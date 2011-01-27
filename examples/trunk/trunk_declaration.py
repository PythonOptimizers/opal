# Description of TRUNK.
from opal.core.algorithm import AlgorithmWrapper
from opal.core.parameter import Parameter
from opal.core.parameter import ParameterConstraint
from opal.core.measure   import Measure

# Define Algorithm object.
trunk = AlgorithmWrapper(name='TRUNK',
                  purpose='Trust Region for UNConstrained problems')

# Register executable command.
trunk.set_executable_command('python trunk_run.py')

# Register parameters.
trunk.add_param(Parameter(name='eta1',
                          kind='real',
                          default=0.25,
                          bound=[0,1],
                          description='Step acceptance threshold'))
trunk.add_param(Parameter(name='eta2',
                          kind='real',
                          default=0.75,
                          bound=[0,1],
                          description='Trust-region increase threashold'))
trunk.add_param(Parameter(name='gamma1',
                          kind='real',
                          default=0.5,
                          bound=[0,1],
                          description='Trust-region shrink factor'))
trunk.add_param(Parameter(name='gamma2',
                          kind='real',
                          default=1.000,
                          bound=[0,1],
                          description='Trust-region moderate shrink factor'))
trunk.add_param(Parameter(name='gamma3',
                          kind='real',
                          default=2.000,
                          bound=[1,None],
                          description='Trust-region increase factor'))
trunk.add_param(Parameter(name='maxit',
                          kind='integer',
                          default=1000,
                          description='Maximum number of iterations'))
trunk.add_param(Parameter(name='stptol',
                          kind='real',
                          default=1.0e-06,
                          description='Stop tolerance'))
trunk.add_param(Parameter(name='rdgrad',
                          kind='real',
                          default=1.0e-05,
                          description='Relative decrease in gradient'))
trunk.add_param(Parameter(name='delta0',
                          kind='real',
                          default=1.000,
                          description='Initial trust-region radius'))
trunk.add_param(Parameter(name='sband',
                          kind='integer',
                          default=5,
                          description='Semi-bandwidth of band preconditioner'))
trunk.add_param(Parameter(name='nmmem',
                          kind='integer',
                          default=10,
                          description='Non-monotone algorithm memory'))
trunk.add_param(Parameter(name='level',
                          kind='real',
                          default=0.1000,
                          description='Level, used for interpolation'))

# Register constraints on the parameters.

trunk.add_parameter_constraint(ParameterConstraint('eta1 < eta2'))
trunk.add_parameter_constraint(ParameterConstraint('eta1 > 0'))
trunk.add_parameter_constraint(ParameterConstraint('eta2 < 1'))
trunk.add_parameter_constraint(ParameterConstraint('gamma1 > 0'))
trunk.add_parameter_constraint(ParameterConstraint('gamma1 <= gamma2'))
#trunk.add_parameter_constraint(ParameterConstraint('gamma2 < 1'))
trunk.add_parameter_constraint(ParameterConstraint('gamma3 > 1'))

# Register atomic measures.
trunk.add_measure(Measure(name='CPU',
                          kind='real',
                          description='Computing time'))
trunk.add_measure(Measure(name='FEVAL',
                          kind='integer',
                          description='Number of function evaluations'))
trunk.add_measure(Measure(name='GEVAL',
                          kind='integer',
                          description='Number of gradient evaluations'))
trunk.add_measure(Measure(name='NITER',
                          kind='integer',
                          description='Number of iterations'))
trunk.add_measure(Measure(name='CGITER',
                          kind='integer',
                          description='Number of CG iterations'))
trunk.add_measure(Measure(name='RDGRAD',
                          kind='real',
                          description='Relative decrease in gradient achieved'))
trunk.add_measure(Measure(name='FVAL',
                          kind='real',
                          description='Final objective function value'))
trunk.add_measure(Measure(name='HEVAL',
                          kind='integer',
                          description='Number of Hessian matrix evaluations'))
#trunk.add_measure(Measure(name='FVAL0',
#                          kind='real',
#                          description='Initial objective function value'))
trunk.add_measure(Measure(name='GNORM',
                          kind='real',
                          description='Gradient 2-norm at final point'))
trunk.add_measure(Measure(name='DELTA',
                          kind='real',
                          description='Final trust-region radius'))
trunk.add_measure(Measure(name='ECODE',
                          kind='integer',
                          description='Exit code'))


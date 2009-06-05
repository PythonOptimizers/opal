
from ..core.testproblem import *

oct_max_aire_d1 = TestProblem(name='oct_max_aire_d1.lp')

QPTest = ProblemCollection(name='QP Test')

QPTest.add_problem(oct_max_aire_d1)

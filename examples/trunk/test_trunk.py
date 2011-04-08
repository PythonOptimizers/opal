# Define a parameter optimization problem in relation to the TRUNK solver.
def test_trunk_optimize():
    from trunk_optimize import prob
    from opal.Solvers import NOMAD

    NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
    NOMAD.solve(blackbox=prob)

if __name__ == '__main__':
    test_trunk_optimize()


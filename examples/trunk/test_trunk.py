# Define a parameter optimization problem in relation to the TRUNK solver.
def test_trunk_optimize():
<<<<<<< HEAD
    from trunk_optimize import prob
    from opal.Solvers import NOMAD

    NOMAD.set_parameter(name='MAX_BB_EVAL', value=10)
    NOMAD.solve(model=prob)
=======
    import trunk_optimize
>>>>>>> master

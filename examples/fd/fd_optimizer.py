from fd_algorithm import compute_error
from math import pi
import pickle
import sys

x = pi/4   # This is where the derivative will be approximated.
cmd = 'python fd_algorithm.py'

def solve(param_file, problem):
    "Run FD with given parameters."

    f = open(param_file, 'rb')
    try:
        parms = pickle.load(f)
    except:
        raise IOError, 'Parameter file does not have expected format'
    f.close()
    h = parms['h'].value

    error = compute_error(x, h)

    return {'ERROR': error}


if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]

    # Solve and gather measures.
    measure_vals = solve(param_file, problem)

    # Write measures to file.
    f = open('FD-' + problem + '.out', 'w')
    for measure in measure_vals:
        print >> f, measure, measure_vals[measure]
    f.close()


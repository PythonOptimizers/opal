from opal.core.io import *
from fd import fd
from math import pi, sin, cos
import sys

f = sin ; df = cos  # Target function and its derivative.
x = pi/4     # This is where the derivative will be approximated.
dfx = df(x)  # "Exact" derivative at x.

def run(param_file, problem):
    "Run FD with given parameters."

    params = read_params_from_file(param_file)
    h = params['h']
    return {'ERROR': abs(dfx - fd(f,x,h))}


if __name__ == '__main__':
    param_file  = sys.argv[1]
    problem     = sys.argv[2]
    output_file = sys.argv[3]

    # Solve, gather measures and write to file.
    measures = run(param_file, problem)
    write_measures_to_file(output_file, measures)


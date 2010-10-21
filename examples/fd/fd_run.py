from fd import fd
from math import pi, sin, cos
import pickle
import sys

f = sin ; df = cos  # Target function and its derivative.
x = pi/4     # This is where the derivative will be approximated.
dfx = df(x)  # "Exact" derivative at x.

def run(param_file, problem):
    "Run FD with given parameters."

    pf = open(param_file, 'rb')
    try:
        parms = pickle.load(pf)
    except:
        raise IOError, 'Parameter file does not have expected format'
    pf.close()
    h = parms['h'].value

    return {'ERROR': abs(dfx - fd(f,x,h))}


if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]
    output_file = sys.argv[3]

    # Solve and gather measures.
    measure_vals = run(param_file, problem)

    # Write measures to file.
    f = open(output_file, 'w')
    for measure in measure_vals:
        print >> f, measure, measure_vals[measure]
    f.close()


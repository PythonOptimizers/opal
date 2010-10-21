from fd import fd
from opal.core.io import *
from math import pi, sin, cos
import pickle
import sys

f = sin ; df = cos  # Target function and its derivative.
x = pi/4     # This is where the derivative will be approximated.
dfx = df(x)  # "Exact" derivative at x.

def run(param_file, problem):
    "Run FD with given parameters."

    #pf = open(param_file, 'rb')
    #try:
    #    parms = pickle.load(pf)
    #except:
    #    raise IOError, 'Parameter file does not have expected format'
    #pf.close()
    params = read_params_from_file(param_file)
    h = params['h']
    return {'ERROR': abs(dfx - fd(f,x,h))}


if __name__ == '__main__':
    param_file  = sys.argv[1]
    problem     = sys.argv[2]
    output_file = sys.argv[3]

    # Solve and gather measures.
    measures = run(param_file, problem)

    # Write measures to file.
    write_measures_to_file(output_file, measures)
    #f = open(output_file, 'w')
    #for measure in measure_vals:
    #    print >> f, measure, measure_vals[measure]
    #f.close()


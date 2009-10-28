# A sample gateway to DFO to be used by Paropt.
# Will be run as 'python dfo_minimizer.py parameter_file problem'
# This version base on cuter interface. Hey

import os
import sys
import pickle
from string import atof

dfo_specFile = 'DFO.SPC'

def write_specfile(parameter_file):
    "Write a valid DFO.SPC given a parameter file."
    # Read parameters into a dictionary
    parms = []
    f = open(parameter_file, 'rb')
    try:
        parms = pickle.load(f)
    except:
        raise IOError, 'Parameter file does not have expected format'
    f.close()

    # Write out DFO.SPC. Parameters must be in order.
    f = open(dfo_specFile, 'w')
    f.write('%10i\n' % parms['NX'].value)
    f.write('%10i\n' % parms['MAXIT'].value)
    f.write('%10i\n' % parms['MAXNF'].value)
    f.write('%10i\n' % parms['STPCRTR'].value)
    f.write('%10.3e\n' % float(parms['DELMIN'].value))
    f.write('%10.3e\n' % float(parms['STPTHR'].value))
    f.write('%10.3e\n' % float(parms['CNSTOL'].value))
    f.write('%10.3e\n' % float(parms['DELTA'].value))
    f.write('%10.3e\n' % float(parms['PP'].value))
    f.write('%10i\n' % parms['SCALE'].value)
    f.write('%10i\n' % parms['IPRINT'].value)
    f.close()
    return

def solve(problem_name):
    os.system('runcuter --package dfo --decode %s > /dev/null' % problem_name)
    f = open('cuter.log', 'r')
    for line in f.xreadlines():
        stats = line.split(':')
        stat = stats[1]
        stat = stat.lstrip()
        stat = stat.rstrip()
        if stat == 'PTIME':
            return [atof(stats[-1])]
    f.close()

if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]
    write_specfile(param_file)
    measure_values = solve(problem)
    for value in measure_values:
        print value,
    print ''

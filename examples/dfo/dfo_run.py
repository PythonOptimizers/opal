# A sample gateway to DFO to be used by OPAL.

import os
import sys
import pickle
from string import atof
from string import atoi
from opal.core.io import *

def write_specfile(parameter_file, loc='.', name='DFO.SPC'):
    "Write a valid DFO.SPC given a parameter file."
    # Read parameters into a dictionary
    parms = read_params_from_file(parameter_file)

    # Write out DFO.SPC. Parameters must be in order.
    f = open(os.path.join(loc, name), 'w')
    f.write('%10i\n' % parms['NX'])
    f.write('%10i\n' % parms['MAXIT'])
    f.write('%10i\n' % parms['MAXNF'])
    f.write('%10i\n' % parms['STPCRTR'])
    f.write('%10.3e\n' % float(parms['DELMIN']))
    f.write('%10.3e\n' % float(parms['STPTHR']))
    f.write('%10.3e\n' % float(parms['CNSTOL']))
    f.write('%10.3e\n' % float(parms['DELTA']))
    f.write('%10.3e\n' % float(parms['PP']))
    f.write('%10i\n' % parms['SCALE'])
    f.write('%10i\n' % parms['IPRINT'])
    f.close()
    return


def solve(problem_name):
    os.chdir(problem_name)
    os.system('./dfomin > run.log')

    ctime = 0.0
    f = open('cuter.log', 'r')
    for line in f.xreadlines():
        line = line.strip('\n')
        if len(line) <= 0:
            continue
        stats = line.split(':')
        stat = stats[1]
        stat = stat.lstrip()
        stat = stat.rstrip()
        if stat == 'PTIME':
            ctime = ctime + atof(stats[-1])
        if stat == 'STIME':
            ctime = ctime + atof(stats[-1])
        if stat == 'FVAL':
            fval = atof(stats[-1])
        if stat == 'NFEVAL':
            nfeval = atoi(stats[-1])
        if stat == 'EXITCODE':
            exitcode = atoi(stats[-1])
        if stat == 'FZERO':
            fzero = atof(stats[-1])
	if stat == 'NCON':
            ncon = atof(stats[-1])

    f.close()
    os.chdir('..')
    return {'EXITCODE' : exitcode,
            'FVAL' : fval,
            'CPU' : ctime,
            'FEVAL' : nfeval*(ncon + 1),
            'DESCENT' : fzero-fval}


def compile_driver(problem_name, log_file='compile.log'):
    if not os.path.exists(problem_name):
        os.system('mkdir %s' % problem)
    os.chdir(problem_name)
    os.system('sifdecode %s > %s 2>&1' % (problem_name, log_file))
    os.system('runcuter --package dfo --keep --blas None --lapack None ' +\
              '> /dev/null')
    os.chdir('..')


if __name__ == '__main__':
    param_file  = sys.argv[1]
    problem     = sys.argv[2]
    output_file = sys.argv[3]

    # Ensure executable is present for current problem.
    executable = os.path.join(problem, 'dfomin')
    if not os.path.exists(executable):
        compile_driver(problem)

    # Ensure spec file is in place and solve.
    write_specfile(param_file, loc=problem)
    measure_values = solve(problem)
    write_measures_to_file(output_file, measure_values)


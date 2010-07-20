# A sample gateway to DFO to be used by OPAL.
# Will be run as 'python dfo_minimizer.py parameter_file problem'

import os
import sys
import pickle
import shutil
from string import atof
from string import atoi

dfo_specFile = 'DFO.SPC'

def write_specfile(parameter_file, problem):
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
    f = open(problem + '/' + dfo_specFile, 'w')
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
    os.chdir(problem_name)
    #os.system('runcuter --package dfo --decode %s > /dev/null' % problem_name)
    #os.system('./' + problem_name + '> run.log')
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
    return {'EXITCODE' : exitcode, 'FVAL' : fval, 'CPU' : ctime,
            'FEVAL' : nfeval*(ncon + 1), 'DESCENT' : fzero-fval}


def compile_driver(problem_name, log_file='compile.log'):
    if not os.path.exists(problem_name):
        os.system('mkdir %s' % problem)
    os.chdir(problem_name)
    os.system('sifdecode %s > %s 2>&1' % (problem_name, log_file))
    os.system('runcuter --package dfo --keep > /dev/null')
    os.chdir('..')
 

if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]

    # Ensure executable is present for current problem.
    executable = os.path.join(problem, 'dfomin')
    if not os.path.exists(executable):
        compile_driver(problem)

    # Ensure spec file is in place and solve.
    write_specfile(param_file, problem)
    #shutil.copy(dfo_specFile,problem)
    measure_values = solve(problem)

    f = open('DFO-'+ problem + '.out','w')
    for measure in measure_values.keys():
        print >> f, measure, measure_values[measure]
    #print >> f,''
    f.close()


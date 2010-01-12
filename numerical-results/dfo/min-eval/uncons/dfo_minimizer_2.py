# A sample gateway to DFO to be used by Paropt.
# Will be run as 'python dfo_minimizer.py parameter_file problem'

import os
import sys
import pickle
import shutil
from string import atof
from string import atoi

dfo_specFile = 'DFO.SPC'

def write_specfile(parameter_file,problem):
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
    #os.system('runcuter --package dfo --decode %s > /dev/null' % problem_name)
    os.chdir(problem_name)
    os.system('./' + problem_name + '> run.log')

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
    return {'EXITCODE': exitcode,'FVAL':fval,'CPU':ctime,'FEVAL':nfeval*(ncon + 1),'DESCENT':fzero-fval}
    
def compile_driver(problem_name,log_file='compile.log'):
    libs = []
    # Order of the libraries is important
    libs.append({'path':'$HOME/opt-package/dfo-ipopt/lib/','name':'dfo_ipopt'})
    libs.append({'path':'$HOME/opt-package/ipopt-fortran/lib','name':'ipopt'})
    libs.append({'path':'$HOME/opt-package/hsl/lib','name':'hsl_ma57'})
    libs.append({'path':'$HOME/opt-package/metis/lib','name':'metis'})
    libs.append({'path':'$HOME/opt-package/lapack/lib','name':'lapack-3.2'})
    libs.append({'path':'$HOME/opt-package/blas/lib','name':'blas-3.2'})
    
    
    driverSource = os.environ['CUTER'] + '/common/src/tools/dfoma.f90'
    linpacObj = os.environ['MYCUTER'] + '/double/bin/linpac.o'
    compiler = 'g95'
    testerDir = problem_name

    if log_file == None:
        indirectStr = ''
    else:
        indirectStr = ' > "' + log_file + '"'

    shutil.copy(linpacObj,testerDir)
    shutil.copy(driverSource,testerDir)
    os.chdir(testerDir)
    (head,tail) = os.path.split(driverSource)

    os.system(compiler + ' -c -I$MYCUTER/double/bin ' +  tail + indirectStr)
    os.system('sifdecode ' + problem_name + indirectStr)
    os.system(compiler + ' -ftrace=full -c *.f' + indirectStr)
    libStr = '-L$MYCUTER/double/lib -lcuter'
    for i in range(len(libs)):
        if libs[i]['path'] != '':
            libStr = libStr + ' -L' + libs[i]['path']
            libStr = libStr + ' -l' + libs[i]['name']
    
    print compiler + ' -o ' + problem_name + ' *.o ' + libStr
    os.system(compiler + ' -ftrace=full -o ' + problem_name + ' *.o ' + libStr + indirectStr)
    os.system('rm -fr *.f *.o')
    os.chdir('..')
    

if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]
    if not os.path.exists(problem):
        os.system('mkdir ' + problem)
        compile_driver(problem)
    write_specfile(param_file,problem)
    #shutil.copy(dfo_specFile,problem)
    measure_values = solve(problem)
    f = open('DFO-'+ problem + '.out','w') 
    for measure in measure_values.keys():
        print >> f, measure, measure_values[measure]
    #print >> f,''
    f.close()

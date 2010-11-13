from opal.core.io import *
from opal.core.tools import *

from distutils.dir_util import copy_tree
import tempfile
import os
import sys
import shutil
import time
import re

src = 'trunk.src'

def get_measures(stats_file):

    measures = {}
    f  = open(stats_file)
    content = f.read()
    f.close()
    measures['CPU'] = extract_measure(content=content,
                                      description='user',
                                      name='CPU',
                                      valueType='real')
    measures['NITER'] = extract_measure(content=content,
                                        description='\#iterations\.*',
                                        name='NITER',
                                        valueType='int')
    measures['CGITER'] = extract_measure(content=content,
                                         description='CG iterations\.*',
                                         name='CGITER',
                                         valueType='int')
    measures['FEVAL'] = extract_measure(content=content,
                                        description='Function evals\.*',
                                        name='FEVAL',
                                        valueType='int')
    measures['GEVAL'] = extract_measure(content=content,
                                        description='Gradient evals\.*',
                                        name='GEVAL',
                                        valueType='int')
    measures['HEVAL'] = extract_measure(
                            content=content,
                            description='Hessian-vector products\.*',
                            name='HEVAL',
                            valueType='int')
    measures['GNORM'] = extract_measure(content=content,
                                        description='Gradient 2-norm\.*',
                                        name='GNORM',
                                        valueType='float')
    measures['RDGRAD'] = extract_measure(
                            content=content,
                            description='Relative decrease in gradient\.*',
                            name='RDGRAD',
                            valueType='float')
    measures['DELTA'] = extract_measure(
                            content=content,
                            description='Final Trust-Region radius\.*',
                            name='DELTA',
                            valueType='float')
    measures['ECODE'] = extract_measure(content=content,
                                        description='Exit code\.*',
                                        name='ECODE',
                                        valueType='int')
    match = re.search('objective value\.*\s:\s+' + \
                          '(?P<FVAL0>-?\d*\.\d+E(\+|-)\d+)/\s+' + \
                          '(?P<FVAL>-?\d*\.\d+E(\+|-)\d+)',
                      content)
    if match is not None:
        measures['FVAL0'] = float(match.groupdict()['FVAL0'])
        measures['FVAL'] = float(match.groupdict()['FVAL'])
    return measures

def write_specfile(params):
    if params is None: # No spc file is created
        return
    f = open('trunk.spc','w')
    f.write('{0:<10d} ## Max. number of iterations         : (I4)\n'\
                .format(params['maxit']))
    f.write('{0:<10.2e} ## Stopping tolerance                : (D7.2)\n'\
                .format(params['stptol']))
    f.write('{0:<10.2e} ## Relative decrease in gradient     : (D7.2)\n'\
                .format(params['rdgrad']))
    f.write('{0:<10.4f} \n'\
                .format(params['eta1']))
    f.write('{0:<10.4f} \n'\
                .format(params['eta2']))
    f.write('{0:<10.4f} \n'\
                .format(params['gamma1']))
    f.write('{0:<10.4f} \n'\
                .format(params['gamma2']))
    f.write('{0:<10.4f} \n'\
                .format(params['gamma3']))
    f.write('{0:<10.4f} ## Initial trust-region radius Delta : (F6.4)\n'\
                .format(params['delta0']))
    f.write("{0:<10} ## Use Powell's rule for Delta       : (L1)\n"\
                .format('F'))
    f.write('{0:<10} ## Use banded preconditioner         : (L1)\n'\
                .format('F'))
    f.write('{0:<10d} ## Semi-bandwidth if preconditioner  : (I4)\n'\
                .format(params['sband']))
    f.write('{0:<10} ## Use a non-monotone strategy       : (L1)\n'\
                .format('F'))
    f.write('{0:<10d} ## Non-monotone algorithm memory     : (I4)\n'\
                .format(params['nmmem']))
    f.write('{0:<10} ## Update Delta using polynomials    : (L1)\n'\
                .format('F'))
    f.write('{0:<10} ## If so, interpolate rho?           : (L1)\n'\
                .format('F'))
    f.write('{0:<10.4f} ## Level, used for interpolation     : (F6.4)\n'\
                .format(params['level']))
    f.write('{0:<10} ## Reentry of GLTR upon rejection    : (L1)\n'\
                .format('F'))
    f.write('{0:<10} ## Display results as Trunk proceeds : (L1)\n'\
                .format('F'))
    f.close()
    return

def run(param_file, problem):
    params = read_params_from_file(param_file)
    curDir = os.getcwd()
    workDir = tempfile.mkdtemp()
    copy_tree(src, workDir)
    os.chdir(workDir)
    write_specfile(params)
    os.system('sifdecode ' + problem + ' > /dev/null')
    os.system('make trunkd > /dev/null')
    os.system('./trunkd > ' + problem + '.sol')
    measures = get_measures(problem + '.sol')
    os.chdir(curDir)
    shutil.rmtree(workDir)
    return measures


if __name__ == '__main__':
    param_file  = sys.argv[1]
    problem     = sys.argv[2]
    output_file = sys.argv[3]

    # Solve, gather measures and write to file.
    measures = run(param_file, problem)
    write_measures_to_file(output_file, measures)


import os
import sys
import pickle
import re
import tempfile
import shutil
from string import atof
from string import atoi
from opal.core.io import *



def extract_measure(content, description, name,
                    valueType = 'int',dem='\s+:\s+'):
    numberPattern = {'int':'-?\d+',
                     'real':'-?\d*\.\d+',
                     'float':'-?\d*\.\d+E(\+|-)\d+'}
    converters = {'int':int,
                  'real': float,
                  'float': float}

    matches = re.finditer(description + dem + '(?P<' +
                          name + '>' +
                          numberPattern[valueType] + ')',
                          content)
    value = None
    for m in matches:
        if name not in m.groupdict().keys():
            raise Exception('Could not to extract measure ' + name)
            continue
        value = converters[valueType](m.groupdict()[name])
    return value

def write_specfile(parameter_file, loc='.', name='ipopt.opt'):
    # Read parameters into a dictionary
    parms = read_params_from_file(parameter_file)

    # Write out ipopt.opt
    f = open(os.path.join(loc, name), 'w')
    for pName in parms:
        f.write( pName + ' ' + str(parms[pName]) + '\n')
    # Fix parameters
    f.write('linear_solver ma57\n')
    f.write('print_level 3\n')
    f.write('print_timing_statistics yes\n')
    f.close()
    return

def get_measures(stats_file, weight=1.0):

    measures = {}
    f  = open(stats_file)
    content = f.read()
    f.close()
    #print content
    measures['CPU'] = extract_measure(
        content=content,
        description='OverallAlgorithm',
        dem='\.*:\s+',
        name='CPU',
        valueType='real')
    measures['HTIME'] = extract_measure(
        content=content,
        description=' UpdateHessian',
        dem='\.*:\s+',
        name='HTIME',
        valueType='real')
    measures['DIRTIME'] = extract_measure(
        content=content,
        description=' ComputeSearchDirection',
        dem='\.*:\s+',
        name='DIRTIME',
        valueType='real')
    measures['PTRTIME'] = extract_measure(
        content=content,
        description=' ComputeAcceptableTrialPoint',
        dem='\.*:\s+',
        name='PTRTIME',
        valueType='real')
    measures['FTIME'] = extract_measure(
        content=content,
        description='Function Evaluations',
        dem='\.*:\s+',
        name='FTIME',
        valueType='real')
    measures['NITER'] = extract_measure(
        content=content,
        description='Number of Iterations',
        dem='\.+:\s+',
        name='NITER',
        valueType='int')
  
    measures['FEVAL'] = extract_measure(
        content=content,
        description='Number of objective function evaluations',
        dem='\s*=\s+',
        name='FEVAL',
        valueType='int')
    measures['GEVAL'] = extract_measure(
        content=content,
        description='Number of objective gradient evaluations',
        dem='\s*=\s+',
        name='GEVAL',
        valueType='int')
    measures['EQCVAL'] = extract_measure(
        content=content,
        description='Number of equality constraint evaluations',
        dem='\s*=\s+',
        name='EQCVAL',
        valueType='int')
    measures['INCVAL'] = extract_measure(
        content=content,
        description='Number of inequality constraint evaluations',
        dem='\s*=\s+',
        name='INCVAL',
        valueType='int')
    measures['EQJVAL'] = extract_measure(
        content=content,
        description='Number of equality constraint Jacobian evaluations',
        dem='\s*=\s+',
        name='EQJVAL',
        valueType='int')
    measures['INJVAL'] = extract_measure(
        content=content,
        description='Number of inequality constraint Jacobian evaluations',
        dem='\s*=\s+',
        name='INJVAL',
        valueType='int')
    measures['ECODE'] = extract_measure(
        content=content,
        description='Exit code',
        dem='\s*=\s+',
        name='ECODE',
        valueType='int')

    measures['WEIGHT'] = weight
    return measures


def run(param_file, problem, keep=False):
    curDir = os.getcwd()
    if not keep:
        workDir = tempfile.mkdtemp()
    else:
        workDir = os.path.join(curDir,problem)
        if not os.path.exists(workDir):
            os.mkdir(workDir)
            
    os.chdir(workDir)
    write_specfile(param_file)
    os.system('sifdecode ' + problem + ' > /dev/null')
    os.system('runcuter -p ipopt > ' + problem + '.sol')
    measures = get_measures(problem + '.sol')
    os.chdir(curDir)
    if not keep:
        shutil.rmtree(workDir)
    return measures

if __name__ == '__main__':
    param_file  = sys.argv[1]
    problem     = sys.argv[2]
    output_file = sys.argv[3]

    # Solve, gather measures and write to file.
    param_file = os.path.abspath(param_file)
    #measures = run(param_file, problem, keep=True)
    measures = run(param_file, problem)
    write_measures_to_file(output_file, measures)



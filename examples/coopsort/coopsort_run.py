import sys
import os

from opal.core.io import *
from opal.core.tools import *

from coopsort import CooperationTreeFactory, coopsort
import sort
import random
import time

def run(param_file, problem):
    N = int(problem)
    params = read_params_from_file(param_file)
    if int(params['nothing']) != 0:
        return {'TIME': float("inf")}
    #print params
    coopTreeFactory = CooperationTreeFactory(name="test factory")
    coopTree = coopTreeFactory.createTreeFromEncodedNumber(name='coop tree',
                                                           encodedNumber=int(params['coopTree']))
    #print coopTree
    l = [int(N * random.random()) for i in xrange(N)]
    t = time.clock()
    l = coopsort(l, coopTree.getRoot())
    measures = {'TIME': time.clock() - t}
    return measures


if __name__ == '__main__':
    param_file  = sys.argv[1]
    problem     = sys.argv[2]
    output_file = sys.argv[3]

    # Solve, gather measures and write to file.
    param_file = os.path.abspath(param_file)
    measures = run(param_file, problem)
    write_measures_to_file(output_file, measures)

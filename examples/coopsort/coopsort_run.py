import sys
import os

from opal.core.io import *
from opal.core.tools import *

from coopsort import CooperationTreeFactory, coopsort
from coopsort import create_test_list, benchmarkTime
import sort
import random
import time


listSpecs = [(8, 1), (8, 0.0125)]


def run(param_file, problem):
    probInfos = problem.split('-')
    listSpecIndex = int(probInfos[0])
    if len(probInfos) > 1:
        listLength = int(probInfos[1])
    else:
        listLength = 4000
    if len(probInfos) > 2:
        numberOfRepeat = int(probInfos[2])
    else:
        numberOfRepeat = 1
    if len(probInfos) > 3:
        groupSize = int(probInfos[3])
    else:
        groupSize = 1
    params = read_params_from_file(param_file)
    if int(params['nothing']) != 0:
        return {'TIME': float("inf")}

    coopTreeFactory = CooperationTreeFactory(name="test factory")
    try:
        treeEncodedNumber = int(params['coopTree'])
    except:
        treeEncodedNumber = int(float(params['coopTree']))
    createTree = coopTreeFactory.createTreeFromEncodedNumber
    coopTree = createTree(name='coop tree',
                          encodedNumber=treeEncodedNumber,
                          radix=6)
    l = []
    for g in range(groupSize):
        l.append(create_test_list(listSpecs[listSpecIndex], listLength, 0))
    meanTime = 0.0
    for r in range(numberOfRepeat):
        sortingTime = 0.0
        for i in range(groupSize):
            l1 = list(l[i])
            tb = benchmarkTime()
            try:
                l1 = coopsort(l1, coopTree.getRoot())
            except:
                return {'TIME': float("inf")}
            te = benchmarkTime()
            sortingTime = sortingTime + (te - tb)
            del l1[:]
            del l1
        meanTime = meanTime + sortingTime

    measures = {'TIME': meanTime / numberOfRepeat}
    return measures


if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]
    output_file = sys.argv[3]

    # Solve, gather measures and write to file.
    param_file = os.path.abspath(param_file)
    measures = run(param_file, problem)
    write_measures_to_file(output_file, measures)

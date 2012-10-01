from coopsort import CooperationTreeFactory, coopsort
from coopsort import create_test_list, benchmarkTime
import sort
import sys

from inspect import isfunction

coopTreeFactory = CooperationTreeFactory(name="test factory")

coopTrees = {}
coopTrees["quick sort"] = sort.quicksort6
coopTrees["merge sort"] = sort.mergesort
coopTrees["radix sort"] = sort.radixsort


benchmarkSpec = {'algorithms': {'coopsort 522': [5, 2, 2],
                                'coopsort 5522522': [5, 5, 2, 2, 5, 2, 2],
                                'coopsort 411': [4, 1, 1]
                                },
                 'lists': {'specs': [(8, 0.0125)],
                           'unit length': 4000,
                           'number of list': 1000
                           },
                 'testing': {'repeats': 100
                             }
                 }

if len(sys.argv) > 1:
    f = open(sys.argv)
    benchmarkSpec = eval(f.read())
    f.close()

algorithms = benchmarkSpec['algorithms']
createAlgo = coopTreeFactory.createTree
for algoName in algorithms:
    coopTrees[algoName] = createAlgo(name='coopsort',
                                     methodSequence=algorithms[algoName])

listSpec = benchmarkSpec['lists']['specs'][0]
listLengh = benchmarkSpec['lists']['unit length']
numberOfList = benchmarkSpec['lists']['number of list']
numberOfRepeat = benchmarkSpec['testing']['repeats']

cpuTime = {}

profiles = {}
for name, coopTree in coopTrees.iteritems():
    profiles[name] = []

for i in range(numberOfList):
    l = create_test_list(listSpec, listLength, 0)
    minTime = float('inf')
    cpuTime = {}
    for name, coopTree in coopTrees.iteritems():
        meanTime = 0.0
        for r in range(numberOfRepeat):
            l1 = list(l)
            if isfunction(coopTree):
                tb = benchmarkTime()
                l1 = coopTree(l1)
            else:
                tb = benchmarkTime()
                l1 = coopsort(l1, coopTree.getRoot())
            te = benchmarkTime()
            del l1[:]
            del l1
            meanTime = meanTime + (te - tb)
        meanTime = meanTime / numberOfRepeat
        cpuTime[name] = meanTime
        if (meanTime < minTime):
            minTime = meanTime

    for name, t in cpuTime.iteritems():
        profiles[name].append(t / minTime)

percentage = [float(i + 1) / numberOfList for i in range(numberOfList)]

for name, x in profiles.iteritems():
    profiles[name] = (sorted(x), percentage)

print profiles

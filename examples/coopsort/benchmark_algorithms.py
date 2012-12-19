from coopsort import CooperationTreeFactory, coopsort
from coopsort import create_test_list, verify_sorted_list, benchmarkTime
import sort
import sys
from inspect import isfunction

coopTreeFactory = CooperationTreeFactory(name="test factory")

coopTrees = {}

coopTrees["quick sort"] = sort.quicksort
coopTrees["quick sort mixed"] = sort.quicksort6
coopTrees["quick sort non-recursive"] = sort.quicksort0
coopTrees["merge sort"] = sort.mergesort
coopTrees['heap sort'] = sort.heapsort
#coopTrees["tim sort"] = sort.timsort

benchmarkSpec = {'algorithms': {'coopsort 522': [5, 2, 2],
                                'coopsort 5522522': [5, 5, 2, 2, 5, 2, 2],
                                'coopsort 411': [4, 1, 1]
                                },
                 'lists': {'specs': [(8, 0.0125)],
                           'unit length': 20,
                           'number of list': 200
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

cpuTime = {}

listSpecs = benchmarkSpec['lists']['specs']
listLenghUnit = benchmarkSpec['lists']['unit length']
numberOfList = benchmarkSpec['lists']['number of list']
numberOfRepeat = benchmarkSpec['testing']['repeats']

for listSpec in listSpecs:
    listType = str(listSpec)
    cpuTime[listType] = {}
    for name, coopTree in coopTrees.iteritems():
        cpuTime[listType][name] = {}
    for k in range(numberOfList):
        n = listLengthUnit * (k + 1)
        l = create_test_list(listSpec, n, 0)
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
                listIsSorted = verify_sorted_list(l1)
                if listIsSorted:
                    meanTime = meanTime + (te - tb)
                else:
                    raise Exception("There is a problem with " + name)
                del l1[:]
                del l1
            cpuTime[listType][name][n] = meanTime / numberOfRepeat
print cpuTime

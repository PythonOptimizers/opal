from coopsort import CooperationTreeFactory, coopsort,  create_test_list, benchmarkTime
import sort
import random
import time
import sys

from inspect import isfunction


coopTreeFactory = CooperationTreeFactory(name="test factory")

coopTrees = {}




# Extract all functions from sort module.
#fcns = [val for key, val in sort.__dict__.iteritems() if isfunction(val)]

# Time.
#for fcn in fcns:

coopTrees["quick sort"] = sort.quicksort6
## coopTrees["coopsort 2"] = coopTreeFactory.createTree(name="quick sort",
##                                                      methodSequence=[2])
## coopTrees['coopsort 522'] = coopTreeFactory.createTree(name='quick sort 1',
##                                                        methodSequence=[5,2,2])
## coopTrees['coopsort 5522522'] = coopTreeFactory.createTree(name='quick sort 2',
##                                                            methodSequence=[5,5,2,2,5,2,2])
## coopTrees['coopsort 555225225522522'] = coopTreeFactory.createTree(name='quick sort 3',
##                                                                    methodSequence=[5,5,5,2,2,5,2,2,5,5,2,2,5,2,2])

coopTrees["merge sort"] = sort.mergesort
## coopTrees["coopsort 1"] = coopTreeFactory.createTreeFromEncodedNumber(name="merge sort",
##                                                                       encodedNumber=1)
## coopTrees['coopsort 411'] = coopTreeFactory.createTree(name='merge sort 1',
##                                                        methodSequence=[4,1,1])
## coopTrees['coopsort 4411411'] = coopTreeFactory.createTree(name='merge sort 2',
##                                                            methodSequence=[4,4,1,1,4,1,1])
## coopTrees['coopsort 444114114411411'] = coopTreeFactory.createTree(name='coopsort',
##                                                                    methodSequence=[4,4,4,1,1,4,1,1,4,4,1,1,4,1,1])

## #coopTrees["insertion sort"] = coopTreeFactory.createTree(name="insertion sort",
## #                                                          methodSequence=[0])

coopTrees["radix sort"] = sort.radixsort
#coopTrees["coopsort 3"] = coopTreeFactory.createTree(name="radix sort",
#                                                     methodSequence=[3])

## #coopTrees['coop sort 1'] = coopTreeFactory.createTree(name='tree 1',
## #                                                      methodSequence=[4,1,2])
#coopTrees['coopsort 4422422'] = coopTreeFactory.createTree(name='coopsort 220910',
#                                                           methodSequence=[4,4,2,2,4,2,2])
coopTrees['coopsort 44224422422'] = coopTreeFactory.createTree(name='coopsort 286315502',
                                                               methodSequence=[4,4,2,2,4,4,2,2,4,2,2])
## Cooptrees['coopsort 12601260014_6'] = coopTreeFactory.createTreeFromEncodedNumber(name='coopsort 12601260014',
##                                                                                 encodedNumber=12601260014,
##                                                                                 radix=6)
## coopTrees['coopsort 5442224422422-1'] = coopTreeFactory.createTree(name='coopsort 1260126001',
##                                                                  methodSequence=[5,4,4,2,2,2,4,4,2,2,4,2,2])
#coopTrees['coopsort 44224522522'] = coopTreeFactory.createTree(name='coopsort 286323314',
#                                                               methodSequence=[4,4,2,2,4,5,2,2,5,2,2])

#coopTrees['coopsort 442242422'] = coopTreeFactory.createTree(name='coopsort 7952846',
#                                                             methodSequence=[4,4,2,2,4,2,4,2,2])
## coopTrees['coopsort 54422312'] = coopTreeFactory.createTree(name='coopsort 270116',
##                                                                 methodSequence=[5,4,4,2,3,1,2])
#n = 8
#listType = 4
cpuTime = {}
if len(sys.argv) > 1:
    listSpec = eval(sys.argv[1])
else:
    listSpec = [8,0.0125]
if len(sys.argv) > 2:
    numberOfList = int(sys.argv[2])
else:
    numberOfList = 100
if len(sys.argv) > 3:    
    listLength = int(sys.argv[3])
else:
    listLength = 4000
if len(sys.argv) > 4:
    numberOfRepeat = int(sys.argv[4])
else:
    numberOfRepeat = 100

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
        #t = time.time()
        #l1 = coopsort(l1, coopTree.getRoot())
        #t = time.time() - t
        meanTime = meanTime/numberOfRepeat
        cpuTime[name] = meanTime
        if (meanTime < minTime):
            minTime = meanTime
        
    for name, t in cpuTime.iteritems():
        profiles[name].append(t/minTime)

percentage = [float(i + 1)/numberOfList for i in range(numberOfList)]

for name, x in profiles.iteritems():
    profiles[name] = (sorted(x), percentage)

print profiles

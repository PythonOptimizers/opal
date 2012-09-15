from coopsort import CooperationTreeFactory, coopsort,  create_test_list, verify_sorted_list, benchmarkTime
import sort
import random
import time
import sys
from inspect import isfunction



coopTreeFactory = CooperationTreeFactory(name="test factory")

coopTrees = {}



coopTrees["quick sort"] = sort.quicksort6
#coopTrees["coopsort 2"] = coopTreeFactory.createTree(name="quick sort",
#                                                     methodSequence=[2])
## coopTrees['coopsort 522'] = coopTreeFactory.createTree(name='quick sort 1',
##                                                        methodSequence=[5,2,2])
## coopTrees['coopsort 5522522'] = coopTreeFactory.createTree(name='quick sort 2',
##                                                            methodSequence=[5,5,2,2,5,2,2])
## coopTrees['coopsort 555225225522522'] = coopTreeFactory.createTree(name='quick sort 3',
##                                                                    methodSequence=[5,5,5,2,2,5,2,2,5,5,2,2,5,2,2])

coopTrees["merge sort"] = sort.mergesort
#coopTrees["coopsort 1"] = coopTreeFactory.createTreeFromEncodedNumber(name="merge sort",
#                                                                      encodedNumber=1)
## coopTrees['coopsort 411'] = coopTreeFactory.createTree(name='merge sort 1',
##                                                        methodSequence=[4,1,1])
## coopTrees['coopsort 4411411'] = coopTreeFactory.createTree(name='merge sort 2',
##                                                            methodSequence=[4,4,1,1,4,1,1])
## coopTrees['coopsort 444114114411411'] = coopTreeFactory.createTree(name='coopsort',
##                                                                    methodSequence=[4,4,4,1,1,4,1,1,4,4,1,1,4,1,1])

#coopTrees["insertion sort"] = coopTreeFactory.createTree(name="insertion sort",
#                                                          methodSequence=[0])

coopTrees["radix sort"] = sort.radixsort
#coopTrees["coopsort 3"] = coopTreeFactory.createTree(name="radix sort",
#                                                      methodSequence=[3])

#coopTrees['coop sort 1'] = coopTreeFactory.createTree(name='tree 1',
#                                                      methodSequence=[4,1,2])
coopTrees['coopsort 4422422'] = coopTreeFactory.createTree(name='coopsort 220910',
                                                           methodSequence=[4,4,2,2,4,2,2])
coopTrees['coopsort 44224422422'] = coopTreeFactory.createTree(name='coopsort 286315502',
                                                               methodSequence=[4,4,2,2,4,4,2,2,4,2,2])
#coopTrees['coopsort 44224522522'] = coopTreeFactory.createTree(name='coopsort 286323314',
#                                                               methodSequence=[4,4,2,2,4,5,2,2,5,2,2])
coopTrees['coopsort 442242422'] = coopTreeFactory.createTree(name='coopsort 7952846',
                                                             methodSequence=[4,4,2,2,4,2,4,2,2])
## coopTrees['coopsort 4422422'] = coopTreeFactory.createTree(name='coopsort',
##                                                       methodSequence=[4,4,2,2,4,2,2])
## coopTrees['coopsort 444224224422422'] = coopTreeFactory.createTree(name='coopsort',
##                                                       methodSequence=[4,4,4,2,2,4,2,2,4,4,2,2,4,2,2])
## coopTrees['coopsort 12601260014_6'] = coopTreeFactory.createTreeFromEncodedNumber(name='coopsort 12601260014',
##                                                                                 encodedNumber=12601260014,
##                                                                                 radix=6)
## coopTrees['coopsort 5442224422422-1'] = coopTreeFactory.createTree(name='coopsort 1260126001',
##                                                                  methodSequence=[5,4,4,2,2,2,4,4,2,2,4,2,2])
## coopTrees['coopsort 5442224422422'] = coopTreeFactory.createTree(name='coopsort 1260126001',
##                                                                  methodSequence=[5,4,4,2,2,2,4,4,2,2,4,2,2])

coopTrees["tim sort"] = sort.timsort


#n = 8
#listType = 4
cpuTime = {}
if len(sys.argv) > 1:
    listSpecs = eval(sys.argv[1])
else:
    listSpecs = [[8,0.0125]]
if len(sys.argv) > 2:
    numberOfList = int(sys.argv[2])
else:
    numberOfList = 200
if len(sys.argv) > 3:    
    listLengthUnit = int(sys.argv[3])
else:
    listLengthUnit = 20

if len(sys.argv) > 4:    
    numberOfRepeat = int(sys.argv[4])
else:
    numberOfRepeat = 50

for listSpec in listSpecs:
    #listType = listSpec[0]
    listType = str(listSpec)
    cpuTime[listType] = {}
    for name, coopTree in coopTrees.iteritems():
        cpuTime[listType][name] = {}
        #print coopTree._name, ',',
        #for n in [7, 8, 9, 10, 11]:
    for k in range(numberOfList):
        n = listLengthUnit*(k+1)
        #for n in [250, 500, 750, 1000, 1250, 1500, 1750, 2000]:
        l = create_test_list(listSpec, n, 0)
        for name, coopTree in coopTrees.iteritems():
            meanTime = 0.0
            for r in range(numberOfRepeat):    
                l1 = list(l)
                #print "Original list of length", len(l1), " is a sorted list:", verify_sorted_list(l1)  
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
                #print name, "worked well:", listIsSorted
                else:
                    raise Exception("There is a problem with " + name)
                del l1[:]
                del l1
            cpuTime[listType][name][n] = meanTime/numberOfRepeat
           
        #print ''
    #print '================'
print cpuTime

#l = [int((N) * random.random()) for i in xrange(N)]
## l = create_test_list(listType, n)
## t = time.time()
## l = sort.quicksort5(l)
## t = time.time() - t

## print 'Quick sort Computing time: %6.4f second \n' %  (t)

## #l = [int((N) * random.random()) for i in xrange(N)]
## l = create_test_list(listType, n)
## t = time.time()
## l = sort.mergesort(l)
## t = time.time() - t

## print 'Merge sort Computing time: %6.4f second \n' %  (t)

## #l = [int((N) * random.random()) for i in xrange(N)]
## l = create_test_list(listType, n)
## t = time.time()
## l = sort.radixsort(l)
## t = time.time() - t

## print 'Radix sort Computing time: %6.4f second \n' %  (t)


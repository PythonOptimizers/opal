from coopsort import CooperationTreeFactory, coopsort,  create_test_list
import sort
import random
import time
import sys



# Extract all functions from sort module.
#fcns = [val for key, val in sort.__dict__.iteritems() if isfunction(val)]

# Time.
#for fcn in fcns:
 


coopTreeFactory = CooperationTreeFactory(name="test factory")

coopTrees = {}

coopTrees["quick sort"] = coopTreeFactory.createTree(name="quick sort",
                                                     methodSequence=[2])
coopTrees["merge sort"] = coopTreeFactory.createTreeFromEncodedNumber(name="merge sort",
                                                                      encodedNumber=1)
#coopTrees["insertion sort"] = coopTreeFactory.createTree(name="insertion sort",
#                                                          methodSequence=[0])
coopTrees["radix sort"] = coopTreeFactory.createTree(name="radix sort",
                                                      methodSequence=[3])
#coopTrees['coop sort 1'] = coopTreeFactory.createTree(name='tree 1',
#                                                      methodSequence=[4,1,2])
coopTrees['coopsort 4422422'] = coopTreeFactory.createTree(name='coopsort',
                                                      methodSequence=[4,4,2,2,4,2,2])
coopTrees['coopsort 444224224422422'] = coopTreeFactory.createTree(name='coopsort',
                                                      methodSequence=[4,4,4,2,2,4,2,2,4,4,2,2,4,2,2])
coopTrees['coopsort 5442224422422'] = coopTreeFactory.createTreeFromEncodedNumber(name='coopsort 12601260014',
                                                                                encodedNumber=12601260014,
                                                                                radix=6)
#coopTrees['optimal coopsort'] = coopTreeFactory.createTreeFromEncodedNumber(name='coopsort',
#                                                                            encodedNumber=4542052244022)
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

generatedLists = {}
for listSpec in listSpecs:
    listType = listSpec[0]
    for k in range(numberOfList):
        n = listLengthUnit*(k+1)
        #for n in [250, 500, 750, 1000, 1250, 1500, 1750, 2000]:
        listName = str(listSpec) + 'l' + str(n)
        generatedLists[listName] = create_test_list(listSpec, n, 0)       
print generatedLists

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


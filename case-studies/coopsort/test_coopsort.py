from coopsort import CooperationTreeFactory, coopsort
import sort
import random
import time

N = 20

# Extract all functions from sort module.
#fcns = [val for key, val in sort.__dict__.iteritems() if isfunction(val)]

# Time.
#for fcn in fcns:

coopTreeFactory = CooperationTreeFactory()
coopTrees = {}
#coopTrees["quick sort"] = CooperationTree(name="quick sort",
#                                          methodSequence=[sort.quicksort])
coopTrees["quick sort"] = coopTreeFactory.createTree(name="quick sort",
                                                     methodSequence=[2])
#coopTrees["bubble sort"] = CooperationTree(name="bubble sort",
#                                           methodSequence=[sort.bubblesort])
#coopTrees["heap sort"] = CooperationTree(name="heap sort",
#                                         methodSequence=[6])
coopTrees["merge sort"] =  coopTreeFactory.createTreeFromEncodedNumber(name="merge sort",
                                                                       encodedNumber=1)
#coopTrees["selection sort"] =  CooperationTree(name="selection sort",
#                                           methodSequence=[7])
coopTrees["insertion sort"] =  coopTreeFactory.createTree(name="insertion sort",
                                                          methodSequence=[0])
coopTrees["radix sort"] =  coopTreeFactory.createTree(name="radix sort",
                                                      methodSequence=[3])
#coopTrees["tim sort"] =  CooperationTree(name="tim sort",
#                                           methodSequence=[8])
coopTrees['coop sort 1'] = coopTreeFactory.createTree(name='test tree 1',
                                                      methodSequence=[4,2,3])
coopTrees['coop sort 2'] = coopTreeFactory.createTree(name='test tree 2',
                                                      methodSequence=[4,4,2,3,3])
#coopTrees['coop sort 2'] = coopTreeFactory.createTree(name='test tree 2',
#                                                      methodSequence=[4,4,2,3,3])
coopTrees['coop sort 3'] = coopTreeFactory.createTreeFromEncodedNumber(name='test tree 3',
                                                                       encodedNumber=45203)

for name, coopTree in coopTrees.iteritems():
    l = [int(N * random.random()) for i in xrange(N)]
    #print "original list", l
    t = time.clock()
    l = coopsort(l, coopTree.getRoot())
    t = time.clock() - t
    #print "after sorting", l
    print '%15s  %6.2f' % (coopTree._name, t)

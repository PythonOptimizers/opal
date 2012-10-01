import sort
import random


class CooperationTreeNode:
    def __init__(self, method=None, **kwargs):
        self._left = None
        self._right = None
        self._method = method
        self._name = None
        return

    def isLeafNode(self):
        return ((self._left is None) and (self._right is None))

    def getMethod(self):
        return self._method

    def getChildren(self):
        return (self._left, self._right)

    def addChildren(self, leftChild, rightChild):
        self._left = leftChild
        self._right = rightChild
        return


class CooperationTree:
    def __init__(self,
                 name='coop-tree',
                 root=None,
                 **kwargs):
        self._root = root
        self._name = name
        return

    def getRoot(self):
        return self._root


class CooperationTreeFactory:
    """
    An object of this class is used to create cooperation trees.
    """
    def __init__(self, name="CooperationTreeFactory", mapping=None):

        self._mapping = {}
        if mapping is None:
            # Initialize by default
            self._mapping[0] = (0, sort.insertionsort)
            self._mapping[1] = (0, sort.mergesort)
            self._mapping[2] = (0, sort.quicksort6)
            self._mapping[3] = (0, sort.radixsort)
            self._mapping[4] = (1, split)
            self._mapping[5] = (1, decompose)
            self._mapping[6] = (0, sort.heapsort)
            self._mapping[7] = (0, sort.selectionsort)
            self._mapping[8] = (0, sort.timsort)
        else:
            self._mapping.update(mapping)
        self._name = name
        return

    def createTree(self,
                   name="CoopTree",
                   methodSequence=[2]):  # quicksort by default
        nodeStack = []
        methodSequence.reverse()
        for m in methodSequence:
            methodType = self._mapping[m][0]
            method = self._mapping[m][1]
            treeNode = CooperationTreeNode(method=method)
            if methodType == 1 and len(nodeStack) > 1:
                # the current method is a decomposition method
                # Pop two nodes from stack and plug into current node
                # as left and right
                leftTree = nodeStack.pop()
                rightTree = nodeStack.pop()
                treeNode.addChildren(leftTree, rightTree)
            # Push the new node to the stack
            nodeStack.append(treeNode)
        # The root tree now is the head of stack
        tree = CooperationTree(name=name, root=nodeStack.pop())
        return tree

    def createTreeFromEncodedNumber(self,
                                    name="CoopTree",
                                    encodedNumber=2,  # Quick sort
                                    radix=6):
        keySequence = []
        q = encodedNumber
        if q == 0:
            return self.createTree(name=name, methodSequence=[0])
        while q != 0:
            keySequence.append(q % radix)
            q = q / radix
        keySequence.reverse()
        #print keySequence
        return self.createTree(name=name, methodSequence=keySequence)


def split(l, *args):
    midpoint = len(l) / 2
    l1 = l[0:midpoint]
    l2 = l[midpoint:]
    return l1, l2


def concatenate(l1, l2):
    l = []
    l.extend(l1)
    l.extend(l2)
    return l


def merge(l1, l2):
    l = []
    p1, p2 = 0, 0
    #print "before merging", l1, l2
    while p1 < len(l1) and p2 < len(l2):
        if l1[p1] < l2[p2]:
            l.append(l1[p1])
            p1 += 1
        else:
            l.append(l2[p2])
            p2 += 1
    if p1 < len(l1):
        l.extend(l1[p1:])
    else:
        l.extend(l2[p2:])
    #print "after merging", l
    return l


def decompose(l, *args):
    if len(l) == 0:
        return [], []
    cutValue = l[0]
    l1 = []
    l2 = []
    for elem in l:
        if elem <= cutValue:
            l1.append(elem)
        else:
            l2.append(elem)
    return l1, l2


def get_inverse(method):
    if method.__name__ == "decompose":
        return concatenate
    if method.__name__ == "split":
        return merge
    return method


def encode(number, base):
    numberStr = ''
    if number == 0:
        return '0'
    while number > 0:
        (number, r) = divmod(number, base)
        numberStr = str(r) + numberStr
    return numberStr


def decode(numberStr, base):
    invertedStr = numberStr[::-1]
    number = 0
    quotient = 1
    for c in invertedStr:
        number = number + int(c) * quotient
        quotient = quotient * base
    return number


def coopsort(l, currentNode):
    """
    l a list of elements to be sorted
    t a cooperation tree.

    The coopsort algorithm will traverse the provided cooperation tree and
    apply the method specified by the node on the associated list. The
    method specified by a node can be a decomposition method or a sort
    method.

    """

    if currentNode.isLeafNode():
        sortMethod = currentNode.getMethod()
        l = sortMethod(l)
        #print "sorted by", sortMethod.__name__, l
        return l
    else:
        decomposeMethod = currentNode.getMethod()
        l1, l2 = decomposeMethod(l)
        #print decomposeMethod.__name__, "the list into", l1, l2
        t1, t2 = currentNode.getChildren()
        l1 = coopsort(l1, t1)
        l2 = coopsort(l2, t2)
        mergeMethod = get_inverse(decomposeMethod)
        l = mergeMethod(l1, l2)
        #print mergeMethod.__name__, "two sorted list to get", l
    return l


def create_test_list(listSpec, n, radix=2):
    '''
    generate a list for testing a sorting algorithm, there 6 type of list
    0: a random list
    1: a sorted list
    2: a list whose 95% sorted
    3: a random list of grand number
    4: an alternative list that is difficult for merge sort,
       for example [0,2,1,3], [0,4,2,6,1,5,3,7]
    '''
    l = []
    listType = listSpec[0]
    if radix > 1:
        N = radix ** n
    else:
        N = n
    if listType == 0:
        l = [int(N * random.random()) for i in xrange(N)]
    elif listType == 1:
        l = [i for i in xrange(N)]
    elif listType == 2:
        N1 = int(0.95 * N)
        l = [i for i in xrange(N)]
        l.extend([int(N * random.random()) for i in xrange(N - N1)])
    elif listType == 3:
        l = [int(10 ** 15 * random.random()) for i in xrange(N)]
    elif listType == 4:
        l = [0, 1]
        for i in range(n - 1):
            l = [j * 2 for j in l]
            l.extend([j + 1 for j in l])
    elif listType == 5:  # gauss distribution mu = 0.5, sigma = 1
        l = [int(N / 2 + N * random.gauss(0, 0.01) / 2) for i in xrange(N)]
    elif listType == 6:  # log-normal distribution
        l = [int(N * random.lognormvariate(0, 10)) for i in xrange(N)]
    elif listType == 7:  # exponential distribution
        l = [int(N * random.expovariate(140)) for i in xrange(N)]
    elif listType == 8:  # gauss distribution mu = 0.5, sigma = 1
        mu = 0
        if len(listSpec) > 1:
            stdVariance = listSpec[1]
        else:
            stdVariance = 0.0125
        l = [int(N / 2 + N * random.gauss(mu, stdVariance) / 2)
             for i in xrange(N)]
        minValue = min(l)
        l = [elem - minValue for elem in l]
    elif listType == 9:  # gauss distribution mu = 0.5, sigma = 1
        mu = 0
        if len(listSpec) > 1:
            stdVariance = listSpec[1]
        else:
            stdVariance = 1
        l = [random.gauss(mu, stdVariance) for i in xrange(N)]
    return l


def verify_sorted_list(l):
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]:
            return False
    return True


from time import time as benchmarkTime

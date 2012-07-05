import sort

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
            self._mapping[2] = (0, sort.quicksort)
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
                   methodSequence=[2]): # quicksort by default
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
                                    encodedNumber=2,
                                    radix=10): # Quick sort
        keySequence = []
        q = encodedNumber
        if q == 0:
            return [0]
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
    p1, p2 = 0,0
    #print "before merging", l1, l2
    while p1 < len(l1) and p2 < len(l2):
        if l1[p1] < l2[p2]:
            l.append(l1[p1])
            p1+=1
        else:
            l.append(l2[p2])
            p2+=1
    if p1 < len(l1):
        l.extend(l1[p1:])
    else:
        l.extend(l2[p2:])
    #print "after merging", l
    return l

def decompose(l, *args):
    cutValue = l[len(l)/2]
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
        print "sorted by", sortMethod.__name__, l
        return l
    else:
        decomposeMethod = currentNode.getMethod()
        l1, l2 = decomposeMethod(l)
        print decomposeMethod.__name__, "the list into", l1, l2
        t1, t2 = currentNode.getChildren()
        l1 = coopsort(l1, t1)
        l2 = coopsort(l2, t2)
        mergeMethod = get_inverse(decomposeMethod)
        l = mergeMethod(l1, l2)
        print mergeMethod.__name__, "two sorted list to get", l
    return l

       

##############################################################
########## For non-recursive coopsort ########################
    
class ConcatenationExpression:
    """
    Contain a concatenation expression in prefix. The operands are a list,
    the operators can be one of two choice: SimpleConcatenation and
    BucketConcatenation
    """

    def __init__(self):
        self._element_stack = []
        self._current_state = 0

    def appendOperand(self, l):
        self._current_state = self._current_state + 1
        print "append operand ", l, "with state", self._current_state
        self._element_stack.append((l, self._current_state))
        return

    def appendOperator(self, op):
        print "append operator ", op.__name__
        self._current_state = 0
        self._element_stack.append((op, self._current_state))

    def evaluate(self):
        l3 = None
        if len(self._element_stack) == 1 and self._current_state == 1:
            l3 = self._element_stack.pop()[0]
            print "final evaluation", l3
            return l3
        while self._current_state == 2:
            l1 = self._element_stack.pop()[0]
            l2 = self._element_stack.pop()[0]
            op = self._element_stack.pop()[0]
            l3 = op(l1, l2)
            currLen = len(self._element_stack)
            if currLen > 0:
                self._current_state = self._element_stack[currLen-1][1]
            else:
                self._current_state = 0
            self.appendOperand(l3)
        print "partial evaluation", l3
        return l3

def nonrecursive_coopsort(l, t):
    """
    l a list of elements to be sorted
    t a cooperation tree.

    The coopsort algorithm will traverse the provided cooperation tree and
    apply the method specified by the node on the associated list. The
    method specified by a node can be a decomposition method or a sort
    method.

    """

    # The traverse tree algorithm in deep-first order and implemented
    # without a recursion. A state stack is required for the implementation
    # of the traverse algorithm
    # A state includes a tree node and the associated list
    stateStack = [(t.getRoot(), l)]

    # the sorted sublists keep the segments that are sorted in the previous
    # visit. If there is two sorted list, a concatenation method is called
    # to get a bigger sublist. The new sublist will replaced the two
    # sublists in the sortedSublists
    concatenationExpression = ConcatenationExpression()
    while len(stateStack) > 0:
        currentNode, currentList = stateStack.pop()
        if currentNode.isLeafNode():
            sortMethod = currentNode.getMethod()
            concatenationExpression.appendOperand(sortMethod(currentList))
            l = concatenationExpression.evaluate()
            print l
        else:
            decomposeMethod = currentNode.getMethod()
            l1, l2 = decomposeMethod(currentList)
            print l1, l2
            t1, t2 = currentNode.getChildren()
            stateStack.append((t2, l2))
            stateStack.append((t1, l1))
            concatenationExpression.appendOperator(get_inverse(decomposeMethod))
    l = concatenationExpression.evaluate()
    return l
    
            

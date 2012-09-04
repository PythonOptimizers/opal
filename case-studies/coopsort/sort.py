# All sorts of sorts in Python.
# D. Orban, Dec 2011.

from heapq import heappush, heappop


def bubblesort(arr):
    done = False
    while not done:
        done = True
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                done = False
    return arr


# From http://docs.python.org/library/heapq.html#basic-examples
def heapsort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for i in xrange(len(h))]


# From
# http://www.koders.com/python/fid6939480467E643A066728A16534C72A951D012A4.aspx?s=mergesort#L3
def mergesort(l):
    if len(l)>1 :
        lleft = mergesort(l[:len(l)/2])
        lright = mergesort(l[len(l)/2:])
        #do merge here
        p1,p2,p = 0,0,0
        while p1<len(lleft) and p2<len(lright):
            if lleft[p1]<lright[p2]:
                l[p]=lleft[p1]
                p+=1
                p1+=1
            else:
                l[p]=lright[p2]
                p+=1
                p2+=1
        if p1 < len(lleft):
            l[p:]=lleft[p1:]
        else:
            l[p:]=lright[p2:]
    return l


# From http://www.daniweb.com/software-development/python/code/216689
def selectionsort(l):
    for i in xrange(0, len(l)):
        min = i
        for j in xrange(i+1, len(l)):
            if l[j] < l[min]:
                min = j
        l[i], l[min] = l[min], l[i]  # swap
    return l

def insertionsort(l):
    for i in xrange(1, len(l)):
        save = l[i]
        j = i
        while j > 0 and l[j - 1] > save:
            l[j] = l[j - 1]
            j -= 1
        l[j] = save
    return l


def quicksort(a):
    # From http://www.daniweb.com/software-development/python/code/216689
    if len(a) <= 1: return a
    pivot = a.pop()
    before = [x for x in a if x <= pivot]
    after = [x for x in a if x > pivot]
    return quicksort(before) + [pivot] + quicksort(after)

def quicksort0(a):
    # non-recursive
    if len(a) <= 1: return a
    stack = []
    sortedList = []
    stack.append(a)
    while len(stack) > 0:
        currentList = stack.pop()
        if len(currentList) <= 1:
            sortedList.extend(currentList)
        else:
            pivot = currentList.pop()
            before = [x for x in currentList if x <= pivot]
            after = [x for x in currentList if x > pivot]
            stack.append(after)
            stack.append([pivot])
            stack.append(before)
    return sortedList

def quicksort2(a):
    # From http://www.daniweb.com/software-development/python/code/216689
    return a if len(a) <= 1 else \
            quicksort([x for x in a[1:] if x <= a[0]]) + \
            [a[0]] + quicksort([x for x in a[1:] if x > a[0]])


def quicksort3(a):
    # From http://www.daniweb.com/software-development/python/code/216689
    if len(a) <= 1: return a
    pivot = a.pop()
    before = [x for x in a if x <= pivot]
    after = [x for x in a if x > pivot]
    try:
        ll = quicksort3(before)
    except:
        ll = insertionsort(before)

    try:
        rl = quicksort3(after)
    except:
        rl = insertionsort(after)      
    return ll + [pivot] + rl

def quicksort4(a):
    # From http://www.daniweb.com/software-development/python/code/216689
    if len(a) <= 1: return a
    pivot = a.pop()
    before = [x for x in a if x <= pivot]
    after = [x for x in a if x > pivot]
    try:
        ll = quicksort4(before)
    except:
        ll = bubblesort(before)

    try:
        rl = quicksort4(after)
    except:
        rl = bubblesort(after)      
    return ll + [pivot] + rl

def quicksort5(a):
    # From http://www.daniweb.com/software-development/python/code/216689
    if len(a) <= 1: return a
    pivot = a.pop()
    before = [x for x in a if x <= pivot]
    after = [x for x in a if x > pivot]
    try:
        ll = quicksort5(before)
    except:
        ll = radixsort(before)

    try:
        rl = quicksort5(after)
    except:
        rl = radixsort(after)      
    return ll + [pivot] + rl

def quicksort6(a):
    # From http://www.daniweb.com/software-development/python/code/216689
    if len(a) <= 1: return a
    pivot = a.pop()
    before = [x for x in a if x <= pivot]
    after = [x for x in a if x > pivot]
    try:
        ll = quicksort6(before)
    except:
        ll = quicksort0(before)

    try:
        rl = quicksort6(after)
    except:
        rl = quicksort0(after)      
    return ll + [pivot] + rl

# From
# http://www.koders.com/python/fid6939480467E643A066728A16534C72A951D012A4.aspx?s=mergesort#L3
def countsort(l, k):
    """A simple counting sort.
    "l" is the list of integers which will be sorted.
    "k" is the range of integers, all numbers in l must be between 0 and k.
    """
    counter = [0]*k
    for x in l:
        counter[x] += 1
    for j in range(1,k):
        counter[j] = counter[j-1] + counter[j]
    for x in reversed(l[:]):
        l[counter[x]-1] = x
        counter[x] -= 1
    return l


def radixsort(l, r=8, k=0):
    """
    l must be a list of integers
    r is the number of bits of a "bin", probably 4 or 8, should be able to
    divide 32 exactly
    k is the upper limit integer of a bin, for countSort. If it's zero, will be
    calculated from r.
    """
    if k==0:
        k=2**r
    mask = int('1'*r, 2)
    for i in range(0, 64/r):
        counter = [0]*k
        for x in l:
            counter[(x>>(i*r)) & mask] += 1
        for j in range(1,k):
            counter[j] = counter[j-1] + counter[j]
        for x in reversed(l[:]):
            l[counter[(x>>(i*r)) & mask]-1] = x
            counter[(x>>(i*r)) & mask] -= 1
    return l


# Timsort is the default for Python lists.
def timsort(l):
    l.sort()
    return l


    

if __name__ == '__main__':
    l = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    timsort(l)
    print l
    print bubblesort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
    print radixsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0], 2)
    print quicksort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
    print quicksort2([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
    l = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    selection_sort(l)
    print l
    l = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
    insertion_sort(l)
    print l
    print mergesort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
    print heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])
    print countsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0], 10)

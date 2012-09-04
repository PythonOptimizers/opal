from sort import radixsort
import random
import time

if __name__ == "__main__":
    N = 20
    l = [int((N + 10**15) * random.random()) for i in xrange(N)]
    l = radixsort(l)
    print "after sorting", [l[i] - l[i+1] for i in range(len(l) -1)]

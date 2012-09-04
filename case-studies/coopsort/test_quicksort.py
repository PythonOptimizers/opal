from sort import quicksort3, quicksort, quicksort5
import random
import time

if __name__ == "__main__":
    N = 20000
    #l = [int((N) * random.random()) for i in xrange(N)]
    l = [i for i in xrange(N)]
    t = time.time()
    l = quicksort5(l)
    t = time.time() - t
    
    #print "after sorting", [l[i] - l[i+1] for i in range(len(l) -1)]
    #print "%6.f"
    print 'Computing time: %6.4f second \n' %  (t)

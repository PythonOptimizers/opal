from inspect import isfunction
import sort
import random
import time

N = 10000

# Extract all functions from sort module.
fcns = [val for key, val in sort.__dict__.iteritems() if isfunction(val)]

# Time.
for fcn in fcns:
    #l = [int(N * random.random()) for i in xrange(N)]
    l = [i for i in xrange(N)]
    #l = [N - i for i in xrange(N)]
    args = ()
    ignoredAlgorithms = ['bubblesort',  'insertionsort',  'selectionsort', 'quicksort2', 'quicksort3', 'quicksort4', 'quicksort5', 'quicksort' ]
    if fcn.__name__ in ignoredAlgorithms:
        continue
    if fcn.__name__ == 'countsort':
        args = (1+max(l),)
    t = time.time()
    fcn(l, *args)
    t = time.time() - t
    print '%15s  %9.5f' % (fcn.__name__, t)

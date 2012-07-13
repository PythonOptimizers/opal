from inspect import isfunction
import sort
import random
import time

N = 100000

# Extract all functions from sort module.
fcns = [val for key, val in sort.__dict__.iteritems() if isfunction(val)]

# Time.
for fcn in fcns:
    l = [int(N * random.random()) for i in xrange(N)]
    args = ()
    if fcn.__name__ == 'bubblesort':
        continue
    if fcn.__name__ == 'countsort':
        args = (1+max(l),)
    t = time.clock()
    fcn(l, *args)
    t = time.clock() - t
    print '%15s  %6.2f' % (fcn.__name__, t)

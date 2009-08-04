import sys

import math
import numpy

from gaussElim import GaussElimination


def get_matrix(matrix_file):
    f = open(matrix_file)
    cells = []
    map(lambda l: cells.extend(l.strip(' \n').split(' ')), f.readlines())
    f.close()
    n = int(math.sqrt(len(cells)))
    matrix = numpy.resize(numpy.array(map(float,cells)),(n,n))
    #print matrix
    return matrix

if __name__ == '__main__':
    '''
    Usage python gf_computing.py pivoting_strategy matrix_file [log_file]
    '''

    gauss_eliminator = GaussElimination(pivottingStrategy=int(sys.argv[1]))
    matrix = get_matrix(sys.argv[2])
    if len(sys.argv) > 3:
        f = open(sys.argv[3],'a')
    else:
        f = open('GE.log','a')
    print >> f, matrix
    #print 
    print >> f, gauss_eliminator.run(matrix)
    print >> f, gauss_eliminator.get_stability()
    print >> f, '---------'
    f.close()
    #print gauss_eliminator.run(matrix)
    print gauss_eliminator.get_stability()

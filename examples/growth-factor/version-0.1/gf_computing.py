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
    Usage python gf_computing.py pivoting_strategy matrix_file
    '''

    gauss_eliminator = GaussElimination(pivottingStrategy=int(sys.argv[1]))
    matrix = get_matrix(sys.argv[2])
    #print matrix
    #print 
    gauss_eliminator.run(matrix)
    print gauss_eliminator.get_stability()

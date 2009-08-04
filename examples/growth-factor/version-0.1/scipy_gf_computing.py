import sys

import math
import numpy

from scipy.linalg import lu


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

    matrix = get_matrix(sys.argv[2])
    print  matrix
    #print 
    print lu(matrix)[2]
    #print gauss_eliminator.run(matrix)

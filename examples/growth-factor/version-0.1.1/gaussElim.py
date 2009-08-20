# this function, swapRows, was adapted from
# Numerical Methods Engineering with Python, Jean Kiusalaas
import numpy

class GaussElimination:
    """
    This object of this class represents for a Gauss elimination 
    that is parameterized by pivotting strategy. Example of usage:
    >>> elimination = GaussElimination(pivottingStrategy=0)
    >>> elmination.run(A)
    The method run() will apply the Gauss elimination process over 
    a matrix A and return the triangular matrix
    After running, we can get some information about the process like
    the stability, the number of iteration ...
    The method run() invokes the Gauss elimiation in batch mode. We 
    can make in run in interactive mode like:
    >>> elimination = GaussEliminiation(pivottingStrategy=1)
    >>> elimination.setData(A)
    >>> elimination.next(A)
    pivotting_strategy = 
    """
    
    TRIVIAL_PIVOTTING = 0
    PARTIAL_PIVOTTING = 1
    COMPLET_PIVOTTING = 2
    
    def __init__(self,pivottingStrategy):
        self.pivotting_strategy = pivottingStrategy
        self.zero = 1.0e-9
        self.verbose = False
        self.iterate = 0
        self.data = None
        self.orgine = None
        self.max_value = 0.0
        pass
    
    def _swapRows(self,i,j):
        """Swaps rows i and j of vector or matrix [v]."""
        temp = self.data[i].copy()
        self.data[i] = self.data[j]
        self.data[j] = temp
        del temp
        return

    def _swapColumns(self,i,j):
        """Swaps rows i and j of vector or matrix [v]."""
        temp = self.data[:,i].copy()
        self.data[:,i] = self.data[:,j]
        self.data[:,j] = temp
        del temp
        return

    def set_data(self,A):
        self.data = numpy.array(A)
        self.origine = numpy.array(A)
        self.max_value =  max(abs(self.data.flatten()))
        return

    def get_pivot(self,k,l):
        #print "before pivotting"
        #print self.data
        maxVal = abs(self.data[k,l])
        n = self.data.shape[0]
        m = self.data.shape[1]
        if self.pivotting_strategy == self.__class__.TRIVIAL_PIVOTTING:
            if self.data[k,l] == 0:
                for i in range(k+1,n):
                    if self.data[i,k] != 0:
                        self._swapRows(i,k)
                        break
        elif self.pivotting_strategy == self.__class__.PARTIAL_PIVOTTING:
            maxIndex = k
            for i in range(k,n):
                if abs(self.data[i,l]) > maxVal :
                    maxVal = abs(self.data[i,l])
                    maxIndex = i
            if maxIndex != k:
                self._swapRows(maxIndex,k)
        else:
            maxRowIndex = k
            maxColumnIndex = l
            for i in range(k,n):
                for j in range(l,m):
                    if abs(self.data[i,j]) > maxVal:
                        maxVal = abs(self.data[i,j])
                        maxRowIndex = i
                        maxColumnIndex = j
            if maxRowIndex != k:
                self._swapRows(maxRowIndex,k)
            if maxColumnIndex != l:
                self._swapColumns(maxColumnIndex,l)
        #print self.data
        #print "Pitvotting", self.data[k,k]
        return self.data[k,l]
                             
    
    def get_stability(self):
        n = self.data.shape[0]
        rho = self.max_value/max(abs(self.origine.flatten()))
        return rho

    def reset(self):
        self.iterate = 0
        del self.data
        self.data = numpy.array(self.origine)
        self.max_value =  max(abs(self.data.flatten()))
        #print self.data
        #print self.max_value
        return
    
    def next(self,iteration = 1):
        if self.iterate == self.data.shape[0]:
            return False
        k = self.iterate
        n = self.data.shape[0]
        p = self.get_pivot(k,k)
        if p == 0:
            self.iterate = self.iterate + 1
            return True
        
        #self.data[k,k:n] = self.data[k,k:n]/p
        for i in range(k+1,n):
            r = self.data[i,k]
            if r != 0:
                self.data[i,k:n] = self.data[i,k:n] - self.data[k,k:n]*r/p
        maxVal =  max(abs(self.data.flatten()))
        if maxVal > self.max_value:
            self.max_value = maxVal
        self.iterate = self.iterate + 1
        #print self.data
        #print self.max_value
        return True

    def run(self,A):
        self.set_data(A)
        self.reset()
        while self.next():
            #print self.data
            pass
        return self.data



   
class TestProblem:
    """
    The abstract class to describe a test problem in most general term
    Every test problem class is a sub-class of this class.
    The most general class contains only the information about the
    test problem: the name
    """
    def __init__(self,name=None,**kwargs):
        self.name = name
        pass

    
class OptimizationTestProblem(TestProblem):
    """
    An abstract class to represent a test problem. Example:

    >>> hs26 = TestProblem(name='HS26', nvar=3, ncon=1)
    >>> print hs26.name, hs26.nvar, hs26.ncon
    HS26 3 1
    """

    def __init__(self, name=None, nvar=0, ncon=0, **kwargs):
        TestProblem.__init__(self,name,**kwargs)
        self.nvar = nvar
        self.ncon = ncon
    
class ProblemSet:
    """
    An abstract class to represent a test set from which lists of
    specific problems may be extracted, and which may be passed to a solver.
    Example:

    >>> HS = ProblemSet(name='Hock and Schittkowski set')
    >>> hs13 = TestProblem(name='HS13', nvar=2, ncon=1)
    >>> hs26 = TestProblem(name='HS26', nvar=3, ncon=1)
    >>> HS.add_problem(hs13)
    >>> HS.add_problem(hs26)
    >>> print [prob.name for prob in HS.problems]
    ['HS13', 'HS26']
    """

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.problems = []       # List of problems in this collection

    def __len__(self):
        return len(self.problems)

    def __getitem__(self,key):
        item = self.problems[key]
        return item

    def __contains__(self,prob):
        return prob in self.problems
    
    def add_problem(self, problem):
        if isinstance(problem, TestProblem):
            self.problems.append(problem)
        else:
            raise TypeError, 'Problem must be a TestProblem'
        
    def all_problems(self):
        """
        Return a list of all problems in this collection.
        """
        return self.problems

class ProblemCollection:
    """
    An abstract class to represet a collection of test problems. A collection is
    made up of subcollections, each of which is a ProblemSet.
    Example:

    >>> HS = ProblemSet(name='Hock and Schittkowski set')
    >>> hs13 = TestProblem(name='HS13', nvar=2, ncon=1)
    >>> hs26 = TestProblem(name='HS26', nvar=3, ncon=1)
    >>> HS.add_problem(hs13)
    >>> HS.add_problem(hs26)
    >>> NCVXQP = ProblemSet(name='Nonconvex Quadratic Programs')
    >>> ncvxqp2 = TestProblem(name='NCVXQP2', nvar=1000, ncon=2500)
    >>> NCVXQP.add_problem(ncvxqp2)
    >>> CUTEr = ProblemCollection(name='CUTEr collection')
    >>> CUTEr.add_subcollection(HS)
    >>> CUTEr.add_subcollection(NCVXQP)
    >>> print [coll.name for coll in CUTEr.subcollections]
    ['Hock and Schittkowski set', 'Nonconvex Quadratic Programs']
    >>> print [prob.name for prob in CUTEr.all_problems()]
    ['HS13', 'HS26', 'NCVXQP2']
    """

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.subcollections = [] # List of subcollections of this collection

    def __len__(self):
        return len(self.allproblems)

    def __getitem__(self,key):
        item = self.allproblems[key]
        return item

    def __contains__(self,prob):
        return prob in self.allproblems
    
    def add_subcollection(self, collection):
        if isinstance(collection, ProblemSet):
            self.subcollections.append(collection)
        else:
            raise TypeError, 'Collection must be a ProblemSet'

    def all_problems(self):
        """
        Return a list of all problems in all subcollections of this collection.
        """
        allprobs = []
        for collection in self.subcollections:
            for prob in collection:
                allprobs.append(prob)
        return allprobs


def _test():
    import doctest
    return doctest.testmod()
            
if __name__ == "__main__":
    _test()


__docformat__ = 'restructuredText'

class TestProblem:
    """
    Abstract class to describe a test problem in general form.
    Every test problem class is a sub-class of this class.
    The ``TestProblem`` class contains only basic information about the
    test problem: the problem name and a description (both strings).
    Example:

    >>> chem=TestProblem(name='Nuke', description='Chemical reactor')
    >>> print chem.name, chem.description
    """

    def __init__(self, name=None, description=None, classifyStr=None,
                 **kwargs):
        self.name = name
        self.description = description
        self.classify_string = classifyStr

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_classify_string(self):
        return self.classify_string


class OptimizationTestProblem(TestProblem):
    """
    An abstract class to represent a test problem in the field of optimization.
    Example:

    >>> hs26 = OptimizationTestProblem(name='HS26', nvar=3, ncon=1)
    >>> print hs26.name, hs26.nvar, hs26.ncon
    HS26 3 1
    """

    def __init__(self, name=None, description=None, classifyStr=None,
                 nvar=0, ncon=0, **kwargs):
        TestProblem.__init__(self, name, description, classifyStr, **kwargs)
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
    >>> print [prob.name for prob in HS]
    ['HS13', 'HS26']

    In the above example, note that a `ProblemSet` is iterable.
    """

    def __init__(self, name=None, **kwargs):
        self.name = name
        self.problems = []       # List of problems in this collection.

    def __len__(self):
        return len(self.problems)

    def __getitem__(self,key):
        return self.problems[key]

    def __contains__(self,prob):
        return (prob in self.problems)

    def add_problem(self, problem):
        "Add problem to collection."
        if isinstance(problem, TestProblem):
            self.problems.append(problem)
        else:
            raise TypeError, 'Problem must be a TestProblem'

    def remove_problem(self, problem):
        "Remove problem from collection."
        if isinstance(problem, TestProblem):
            try:
                self.problems.remove(problem)
            except ValueError:
                pass  # Silently ignore
        else:
            raise TypeError, 'Problem must be a TestProblem'

    def pop_problem(self, i=-1):
        "Return i-th problem (default: last) and remove it from collection."
        if isinstance(problem, TestProblem):
            try:
                self.problems.pop(i)
            except IndexError:
                pass  # Silently ignore
        
    def all_problems(self):
        "Return a list of all problems in this collection."
        return self.problems.copy()
    
    def select(self, query):
        """
        Return the list of problems matching the given query.
        The `query` object is any object that possesses a `match()` method.
        The result of `match(name, string)` must be True if `name` matches
        `string`. During the query, `name` is the problem name and `string`
        is its classification string.
        """
        queryResult = []
        for prob in self.problems:
            if query.match(prob.name, prob.get_classify_string()):
                queryResult.append(prob)
        return queryResult


class ProblemCollection:
    """
    An abstract class to represet a collection of test problems. A collection
    is made up of subcollections, each of which is a `ProblemSet`.

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

    def __init__(self, name=None, description=None, **kwargs):
        self.name = name
        self.description = description
        self.all = ProblemSet('Physic set of the collection. It contains all problem of collection')
        self.subcollections = [] # List of subcollections of this collection

    def __len__(self):
        return len(self.all_problems())

    def __getitem__(self,key):
        return self.all_problems()[key]

    def __contains__(self,prob):
        return (prob in self.all_problems())
    
    def add_subcollection(self, collection):
        "Add a subcollection to this collection."
        if isinstance(collection, ProblemSet):
            self.subcollections.append(collection)
        else:
            raise TypeError, 'Collection must be a ProblemSet'

    def all_problems(self):
        """
        Return a list of all problems in all subcollections of this collection.
        """
        allprobs = self.all
        for collection in self.subcollections:
            allprobs.extend(collection.problems)
        return allprobs

    def select(self,query):
        return self.all.select(query)
        
def _test():
    import doctest
    return doctest.testmod()
            
if __name__ == "__main__":
    _test()

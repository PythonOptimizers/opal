import os

class Solver:

    def __init__(self, name='', command=None, input=None, parameter='',
                 output=None, **kwargs):
        self.name = name
        self.command = command
        self.args = [input, parameter, output]
        return

    #def run(self):
    #    cmdStr = self.command
    #    for argv in self.args:
    #        if argv != None:
    #            cmdStr = cmdStr + ' ' + str(argv)
    #    os.system(cmdStr)
    #    return

    def solve(self, problem, **kwargs):
        """
        The solve method return a process describing the solving process
        according solver's algorithm.
        The solving process is either an iterative process or batch process.
        In the case of an iterative process, the user can interfere to
        solving process in each iteration.
        Otherwise, the user just runs the process and get final result
        Two form of invoking a solver

        >>> solvingProc = aSolver.solve(problem)
        >>> finalResult = solvingProc.run(problem.initial_point)

        >>> solvingProc = aSolver.solve(problem)
        >>> solvingProc.initialize(problem.initial_point)
        >>> while solvingProc.next() :
        >>>   result = solvingProc.get_status()

        The advantage of this appoach is that, the solving process can
        be invoked with different initial information, for example the
        initial point
        """

        return None

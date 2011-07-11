import copy
from data import Data
from tools import TableFormatter

class Measure(Data):
    """
    A Measure object represent for an observation from output of
    algorithm running. It has two aspect
    - Data: its value is value of an observation
    - Functionality: It encapsulates the way to extract measure value
      from the output.
    """

    def __init__(self, name=None, description='', kind=None, **kwargs):
        Data.__init__(self,name=name, description=description, type=kind)
        return


    def get_value(self):
        return


class MeasureValueTable:

    def __init__(self,problem_names,measure_names):

        sortedProblemNames = sorted(problem_names)
        self.measure_names = measure_names
        self.problem_names = sorted(problem_names)
        self.table = {} # this mapping with key is the name of problems
                        # and value is another mapping whose key is measure name
                        # and value is a list of value
                        # We don't use the table because the different measure
                        # have different type
        return


    def __len__(self):
        return (len(self.problem_indices),len(self.measure_names))


    def __getitem__(self,key):

        if type(key) == type(('Problem','Measure')):
            return self.get_cell(key[0],key[1])
        return self.get_column(key)


    def get_cell(self,prob,measure):
        return self.table[problem][measure]


    def get_column(self,measure):

        col = []
        for prob in sorted(self.problem_names):
            col.append(self.table[prob][measure])
        try:
            import numpy
            return numpy.array(col)
        except ImportError:
            import array
            return array.array('d', col)


    def get_row(self,prob):

        row = []
        for measure in sorted(self.measure_names):
            row.append(self.table[prob][measure])
        return row


    def get_problems(self):
        return sorted(self.problem_names)


    def get_measures(self):
        return sorted(self.measure_names)


    def add_problem_measures(self,problem,measure_values):
        self.table[problem] = copy.copy(measure_values)
        return


    def clear(self):
        for problem in self.table.keys(): del self.table[problem]
        return


    def __str__(self, formatter=TableFormatter()):
        return self.toString(formatter=formatter)


    def toString(self, formatter=TableFormatter()):
        tableStr = ''
        headerStr = formatter.set_header(headers=self.measure_names)
        if headerStr is None:
            return None
        tableStr = tableStr + headerStr
        for prob in sorted(self.table.keys()):
            recordStr = formatter.format(prob, self.table[prob])
            if recordStr is not None:
                tableStr = tableStr + recordStr
        return tableStr

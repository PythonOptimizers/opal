import copy

from data import Data
from data import DataTable
from tools import TableFormatter


class Measure(Data):
    '''
    
    A Measure object represent for an observation from output of 
    algorithm running. It has two aspect
    - Data: its value is value of an observation 
    - Functionality: It encapsulates the way to extract measure value 
      from the output.
    '''

    def __init__(self, name=None, description='', kind=None, **kwargs):
        Data.__init__(self, name=name, description=description, type=kind)
        return

class MeasureValueTable(DataTable):
    def __init__(self, name='measure-table', problems=None, measures=None):
        self.problems = problems
        self.measures = measures
        DataTable.__init__(self,
                           name=name,
                           rowIdentities=[prob.identify() for prob in problems],
                           columnIdentities=[measure.identify() \
                                             for measure in measures])
        return 

    def __len__(self):
        return DataTable.__len__(self)

    def __getitem__(self, key):
        if type(key) == type(('Problem','Measure')):
            return self.get_problem_measure(key[0],key[1])
        return self.get_column(key)


    def get_problem_measure(self, problem, measure):
        #print prob,measure,self.table[measure],self.problem_indices[prob]
        return self.table[problem][measure]

    def get_measure_vector(self, measure):
        col = []
        for prob in sorted(self.problem_names):
            col.append(self.table[prob][measure])
        try:
            import numpy
            return numpy.array(col)
        except ImportError:
            import array
            return array.array('d', col)

    def get_problem_measures(self, problem):
        row = []
        for measure in sorted(self.measure_names):
            row.append(self.table[prob][measure])
        return row

    def get_problems(self):
        return sorted(self.problem_names)

    def get_measures(self):
        return sorted(self.measure_names)

    def add_problem_measures(self,problem,measure_values):
        #self.problem_indices[problem] = len(self.problem_indices)
        #print problem,measure_values
        self.table[problem] = copy.copy(measure_values)
        return

    def clear(self):
        for problem in self.table.keys():
            del self.table[problem]
        return

    def __str__(self, formatter=TableFormatter()):
        #print self.table
        #print self.problem_indices
        #print self.measure_names
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


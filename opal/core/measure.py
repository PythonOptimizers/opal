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




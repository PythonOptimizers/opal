"""

This module contains two classes that descriibe two  entities Data and DataSet
Data is one of the two elementary entities in the Data-Operator methodology
DataSet is set of data to described an object. All of data elements have the
same storage and in/out method.
"""
import re
import itertools
import log
from set import Set

class Data:
    """

    Data is one of two elementary entities. It has a name, value type and value.
    The most important methods of this class are `set` and `get`.
    The type of data may be a scalar of type integer, floating number, or
    a vector, a matrix.
    """
    def __init__(self, name='',
                 description='',
                 type='real',
                 dimension=1,
                 value=None,
                 domain=None,
                 *argv,**kwargv):
        self.name = name
        self.description = description
        self.type = type
        self.value = value
        self.dimension = dimension
        self.domain = domain
        self.is_scalar = (self.dimension == 1)
        self.is_real = (self.type == 'real')
        self.is_integer = (self.type == 'integer')
        self.is_binary = (self.type == 'binary')
        if self.is_binary:
            self.domain = [0,1]
        self.is_categorical = (self.type == 'categorical')
        pass

    def identify(self):
        '''

        The method provide the identity of a Data object. By default,
        the name is considered as the identity
        '''
        return self.name

    def set(self, value):
        self.value = value
        return

    def get(self):
        return self.value

    def get_type(self):
        return self.type

    def get_domain(self):
        return self.domain

    def get_dimension(self):
        return self.dimension

class DataSet(Set):
    """

    DataSet set of data elements. It provides one more method in comparing with
    a Set object, the set_values() method. This method to update value of the
    elements belong to set
    """
    def __init__(self,name="", elements=[],
                 *argv,**kwargv):
        self.name = name
        self.indices = {}
        self.db = []
        if len(elements) > 0:
            index = 0
            for elem in elements:
                self.indices[elem.identify()] = index
                self.db.append(elem)
                index = index + 1
        return

    def set_values(self, values=None, *args, **kwargs):
        """

        Use the arguments {\sf values}, {\sf args} and {\sf kwargs} to build
        up a mapping
        from the name to value. After that, the {\sf set_value} method of each
        element is provoked to set value for them.

        This method pemits to set values for a set by the following statements:
        >>> dataSet.set_values(1, 2, 3)
        >>> dataSet.set_values([1, 2, 3])
        >>> dataSet.set_values([1, 2], 3)
            Assign three first elements to 1, 2 and 3.
        >>> dataSet.set_values(values=[1, 2, 3], elem4=4)
            Set first three element to 1, 2 and 3 correspondingly. And set the
            element whose name is elem4 to 4.
        >>> dataSet.set_values(elem5=5)
            Assign 5 to the {\sf elem5} element.

        The following assign is syntaxly correct but raises a logical issue
        >>> dataSet.set_values(1, [2, 3])
        """
        valueList = []
        valueDict = {}
        if (values is not None) :
            # check type of {\sf values} to get correctly the values
            if type(values) == type([]) or type(values) == type((1,)) :
                valueList.extend(values)
            elif type(values) == type({}): # values are provided in form of
                                           # a mapping between identity and
                                           # value
                valueDict.update(values)
            else: # values is an value
                valueList.append(values)
        else:
            valueDict.update(kwargs)

        if (len(valueList) <= 0) and (len(valueDict) <= 0):
            # Set value to the default
            for elem in self.db.values():
                elem.set_value(None)
        else:
            # Set the values in the list first
            for elem, value in itertools.izip(self.db, valueList):
                elem.set(value)
            # The values in the dictionary is added of
            # correct the ones are set by the list
            for elemId in valueDict.keys():
                if elemId in self.indices.keys():
                    self.db[self.indices[elemId]].set(valueDict[elemId])
        return

    def select(self, query):
        '''

        The select is rewritten to return a DataSet object instead of
        Set object
        '''
        queryResult = DataSet(name='query-result')
        for elem in self.db:
            if query.match(elem):
                queryResult.append(prob)
        return queryResult


class DataTable:
    def __init__(self, name, rowIdentities=[], columnIdentities=[]):
        '''

        We suppose that a table is set of D
        '''

        self.name = name
        self.row_identities = rowIdentities
        self.column_identities = columnIdentities
        #log.debugger.log('Row identities: ' + str(self.row_identities))
        #log.debugger.log('Column identities: ' + str(self.column_identities))

        # We store only the valid values like a dense matrix
        # The table is a dictionary of dictionary-column.
        # This means that the coordination of a cell is formed
        # by a tuple whose first element indicates the row(s)
        # and whose second one indicates the column(s). However,
        # the access through the column or row is equivalent
        self.table = {}


        return

    def __len__(self):
        length = 0
        for row in self.table.keys():
            #log.debugger.log(str(self.table[row]))
            length = length + len(self.table[row])
        return length


    def get_formal_length(self):
        #log.debugger.log('row, column: ' +\
        #                 str(len(self.row_identities)) + ', ' +\
        #                 str(len(self.column_identities))
        #                 )
        return len(self.row_identities)*len(self.column_identities)

    def get_size(self):
        '''

        Return a tuple of which each element is the size of a dimension
        '''
        return (len(self.row_identities), len(self.column_identities))

    def __getitem__(self, key):
        if (type(key) == type(('a','tuple'))) or \
           (type(key) == type(['a list'])):
            if len(key) < 0:
                raise Exception("Invalid cell's coordination ")
            row = key[0]
            col = key[1]
        return self.table[row][key]

    def get_storage_ratio(self):
        '''

        Return the ratio between physical length and formal one.
        Base on this ration, we determine the status of a table that
        take one of following four values:

         - Empty: ratio = 0
         - Sparse: ratio <= 0.5
         - Dense: ration > 0.5
         - Complete: ratio = 1
        '''
        #log.debugger.log('Actual length, formal length: ' +\
        #                 str(self.__len__() + 0.0) + ', ' +\
        #                 str(self.get_formal_length() + 0.0)
        #                 )
        ratio =  (self.__len__() + 0.0)/(self.get_formal_length() + 0.0)
        return ratio

    # Row-related operations
    def get_row(self, rowId):
        valueDict = {}
        if rowId not in self.row_identities:
            raise Exception('Row identity is not valid')

        if rowId not in self.table.keys():
            '''

            Return an empty dictionary
            '''
            return valueDict

        for col in self.column_identities:
            if col in self.table[rowId].keys():
                valueDict[col] = self.table[rowId][col]
        return valueDict

    def get_row_keys(self):
        return self.row_identities

    def add_row(self, rowId):
        if rowId in self.row_identities:
            '''

            Do nothing if a row having the same identities exists
            '''
            return
        self.row_identities.append(rowId)
        return

    def update_row(self, rowId, values=None, **kwargs):
        if rowId not in self.row_identities:
            raise KeyError, 'Could identify a row of ID ' + str(rowId)
        if rowId not in self.table.keys():
            self.table[rowId] = {}
        valueDict = {}
        if type(values) is type(['list']):
            for col, val in itertools.izip(self.column_identities, values):
                valueDict[col] = val
        if type(values) is type({'key':'value'}):
            valueDict.update(values)
        valueDict.update(kwargs)
        #log.debugger.log('Values to update: ' + str(valueDict))
        for col, val in valueDict.iteritems():
            self.table[rowId][col] = val
        return

    # Column-related operations

    def get_column(self, colId):
        '''

        Return a dictionary that map row identities and values of
        corresponded cell
        '''
        valueDict = {}
        if colId not in self.column_identities:
            raise Exception('Column identity is not valid')

        for row in self.row_identities:
            if (row in self.table.keys()) and \
                   (colId in self.table[row].keys()):
                valueDict[row] = self.table[row][colId]
        return valueDict

    def get_column_keys(self):
        return self.column_identities

    def add_column(self, colId):
        if colId in self.column_identities:
            return
        self.column_identities.append(colId)

    def update_column(self, colId, values=None, **kwargs):
        if coldId not in self.column_identities:
            raise KeyError, 'Could not identify a column of ID ' + str(colId)

        valueDict = {}

        if type(values) is type(['list']):
            for row, val in itertools.izip(self.row_identities, values):
                valueDict[row] = val
        if type(values) is type({'key':'value'}):
            valueDict.update(values)

        valueDict.update(kwargs)

        for row, val in valueDict.iteritems():
            if row not in self.table.keys():
                self.table[row] = {}
            self.table[row][colId] = val
        return







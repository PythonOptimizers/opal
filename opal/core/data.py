"""

This module contains two classes that descriibe two  entities Data and DataSet
Data is one of the two elementary entities in the Data-Operator methodology
DataSet is set of data to described an object. All of data elements have the
same storage and in/out method.
"""
import re
import itertools
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
            for id in valueDict.keys():
                if name in self.indices.keys():
                    self.db[self.indices[id]].set(valueDict[id])
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
      
class ListExtractor:
    """
    List extractor get an element of the list
    The input list may be a Python list or 
    a string whose word seperated by seperator
    """
    def __init__(self,index=0, seperator=' '):
        self.index = index
        
    def get_value(self,list):
        if self.index < 0:
            return None
        if type(list) == types('a string'):
            realList = list.split(self.seperator)
        elif type(list) == type([]):
            realList = list
        else:
            return None
        if self.index >= len(list):
            return None
        return list[self.index]
        
class TextExtractor:
    """
    An instance of TextExtractor can extract a value 
    basing on the regular expression that build form the
    predefined pattern
    Each instance is distinguished by the his pattern
    """
    def __init__(self,pattern=None,digitPattern=None):
        self.pattern = pattern
        if digitPattern is None:
            self.digit_pattern = '[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?'
        else:
            self.digit_pattern = digitPattern

    def get_value(self, text):
        if text is None:
            return None
        if self.pattern is None:
            return None
        p = re.compile(self.pattern + '.+')
        m = p.search(text)
        if m is None:
            return None
        matchedLine = m.group()
        #print matchedLines.groups()
        #digit_pattern = '-?\d+(\.\d+)?(e-?\d+)?' 
        #m = re.compile(self.digit_pattern).search(matchedLine)
        #if m is None:
        #    return None
        #print m.groups(), m.group()
        #values = re.compile(digit_pattern).findall(matchedLine)
       
        values = []
        for m in re.finditer(self.digit_pattern,matchedLine):
            #print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))
            values.append(m.group(0))
        if len(values) > 1 :
            return values
        if len(values) <= 0:
            return None
        return values[0]
        

"""
This module contains two classes that descriibe two  entities Data and DataSet
Data is one of the two elementary entities in the Data-Operator methodology
DataSet is set of data to described an object. All of data elements have the
same storage and in/out method.
"""
import re

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

    def set(self,value):
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

class DataSet:
    """
    DataSet is a group of data that has common storage and in/out method
    DataDescription object is used to verify the input is valid and create the
    output object.
    Two important static methods are check() and create_data
    There is an object called Any that represents for any data (no constraints or
    requirement). The check() method return True always
    Note that the check() and create_data() is the class methods not static method
    because we want to profit the inheritance over this class
    """
    def __init__(self,name="",storage=None,*argv,**kwargv):
        self.name = name
        self.storage = storage
   
        pass

 
    def load(self):
        pass

    def save(self):
        pass

    @classmethod
    def check(data,*args,**kwargs):
        """
        This virtual function, it is overriden to express the constraints and 
        requirements on the data. It is used mainly in verification of input 
        for a process.
        
        """
        return True
    
    @classmethod
    def create_data(*args,**kwargs):
        return DataSet()

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
        

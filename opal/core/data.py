"""

This module contains two classes that descriibe two  entities Data and DataSet
Data is one of the two elementary entities in the Data-Operator methodology
DataSet is set of data to described an object. All of data elements have the
same storage and in/out method.
"""
import re
import itertools

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
    
    def __getitem__(self, id):
        '''

        A data set object provide two ways to access an element: by order or by
        identity that provided by methode {\sf identify()}
        '''
        if (type(id) == type(0)):
            return self.db[id]
        else:
            return self.db[self.indices[id]]
      
    def __len__(self):
        return len(self.db)

    def __contains__(self, elem):
        '''

        There are two way to verify the existence of an element in a DataSet 
        object.
        Either element or its identity can be provided for the verification.
        '''
        # if this is an empty DataSet object the False signal is returned 
        # immediately
        if len(self.indices) <= 0:
            return False
        indexType = type(self.indices.keys()[0])
        # Identity is provided to the verifcation
        if type(elem) == indexType:
            return (elem in self.indices.keys())
        # Element is provided
        else:
            return (elem.identify() in self.indices.keys())

    def append(self, elem):
        '''

        Add an element to the set
        '''
        # An element with the same name is in the set. Nothing to add
        if elem.identify() in self.indices:
            return 
        self.indices[elem.identify()] = len(self.db)
        self.db.append(elem)
        return

    def remove(self, elem):
        return 

    def set_values(self, values=None, *args, **kwargs):
        """
        
        Use the arguments {\sf values}, {\sf args} and {\sf kwargs} to build
        up a mapping  from the name to value. After that, the {\sf set_value}
        method of each element is provoked to set value for them.
        
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

        The following assign is syntaxly correct but raises a logical issue:

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
                if id in self.indices.keys():
                    self.db[self.indices[id]].set(valueDict[id])
        return

 
   

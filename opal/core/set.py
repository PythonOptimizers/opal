class Set:
    """

    Set is a group of elements distinguished by identity (given by identify()
    method). The Set class cover the apsects of two Python built-in data
    structures: dict and list. It keeps the order of the element like it added
    to Set. This means that we can access an element by its position. Each
    elements in the Set is assigned a key that is actually the identity of
    elements. A requirement applied to the elements of a Set object is each
    element has a method that show its identity.
    """
    def __init__(self,name="", elements=[], *argv, **kwargv):
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
        idType = type(self.indices.keys()[0])
        # Identity is provided to the verifcation
        if type(elem) == idType:
            return (elem in self.indices.keys())
        # Element is provided
        else:
            try:
                return (elem.identify() in self.indices.keys())
            except:
                return False

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
        '''

        Remove an element from the set.
        '''
        if len(self.inidces) <= 0:
            return
        idType = type(self.indices.keys()[0])
        if type(elem) == idType:
            try:
                index = self.indices[elem]
            except:
                raise IndexError
        else:
            try:
                index = self.indices[elem.identify()]
            except:
                raise IndexError
        i = index + 1
        # Update the indices
        while i < len(self.db):
            id = self.db[i].identify()
            self.indices[id] = self.indices[id] - 1
            i = i + 1
        # Remove the element from the database and remove its index
        id = self.db[index].identify()
        self.db.remove(self.db[index])
        del self.indices[id]
        return

    def select(self, query):
        queryResult = Set(name='query-result')
        for elem in self.db:
            if query.match(elem):
                queryResult.append(prob)
        return queryResult

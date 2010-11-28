import re
import logging


class HandlerDescription:
    def __init__(self, handler):
        self.file_name = handler.baseFilename
        self.level = handler.level

    def generate_handler(self):
        handler = logging.FileHandler(filename=self.file_name)
        handler.set_level(self.level)
        return handler

class OPALLogger:
    '''
    
    We specialize logging facility of Python by this class to support 
    the ability of pickling an logger with handlers that are the streamming 
    objects
    '''
    
    def __init__(self, name, handlers=[]):
        self.name = name
        self.initialize()
        # Initialize an empty list of descriptions 
        # of the user-required handlers
        self.handler_descriptions = []
        # Get the description of the user-required handlers
        # and add it to logger
        for hdlr in handlers: 
            self.handler_descriptions.append(HandlerDescription(hdlr))
            self.logger.addHandler(hdlr)
        return
    
    def initialize(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)  # Set level to highest level so 
                                             # that actual level depends on the 
                                             # handler level
        # A default handler is created for logging to file with INFO level
        handler = logging.FileHandler(filename='opal.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s:  %(message)s'))
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        return
    
    def __getstate__(self):
        # To serialize a OPALLogger object, we save only 
        # the name and the descriptions of the user-required handlers
        dict = {}
        dict['handler_descriptions'] = self.handler_descriptions
        dict['name'] = self.name
        return dict

    def __setstate__(self, dict):
        # The expected dict is two-element dictionary.
        # The first element of dict has key is 'handler_descriptions'
        # and has value is a list of description of handlers. The 
        # second one is the name of logger.
        self.name = dict['name']
        # Initialize the logger with the specified name
        self.initialize()
        # Create the handler descriptions for unpickled object
        # and create handlers for the logger
        self.handler_descriptions = dict['handler_descriptions']
        for desc in self.handler_descriptions:
            handler = desc.generate_handler()
            self.logger.addHandler(handler)
        return
        
    def log(self, message, level=logging.INFO):
        self.logger.info(message)
        return
    
    
'''
class TestLogging:
    def __init__(self,**kwarg):
        self.testIdReg = re.compile("# Test number: [0-9]+")
        pass
        
    def write(self,empiricalModel,fileName='test.log'):
        f = open(fileName,'a')
        print >> f, '# Test number:', empiricalModel.test_number
        print >> f, '# Parameters:', [(param.name,param.value) for param in empiricalModel.parameters if not param.is_const()]
        print >> f, '# Non relaxable constraints are violated:', empiricalModel.test_is_failed
        if not empiricalModel.test_is_failed:
            print >> f, '# PROB',
            for m in sorted([measure.name for measure in empiricalModel.measures]):
                print >> f, m,
            print >> f, ''
            print >> f, empiricalModel.measure_value_table.__string__()
        f.close()
        return

    def read(self,fileName,id):
        f = open(fileName)
        content = f.read()
        f.close()

        positions = []
        iters = testIdReg.finditer(content)
        for it in iters:
            positions.append(it.span())

        idReg = re.compile('[0-9]+')
        tests = {}
        for i in range(len(positions)):
            testId = content[positions[i][0]:positions[i][1]]
            ids = idReg.findall(testId)
            if ids[0] == id:
                if i < len(positions) - 1:
                    tests[ids[0]] = (positions[i][0],positions[i+1][0])
                else:
                    tests[ids[0]] = (positions[i][0],None)
                break

        if tests[id][1] is None:
            return content[tests[id][0]:]
        else:
            return content[tests[id][0]:tests[id][1]]

class PythonLogging:
    def __init__(self,**kwarg):
        pass

    def write(self,empiricalModel,fileName='test.log'):
        f = open(fileName,'a')
        print >> f, '# Test number:'
        print >> f, empiricalModel.test_number
        print >> f, '# Parameters:'
        print >> f, [(param.name,param.value) for param in empiricalModel.parameters]
        #print >> f, '# Non relaxable constraints are violated:', empiricalModel.test_is_failed
        if not empiricalModel.test_is_failed:
            print >> f, '# Table format'
            print >> f, "{ 'PROB' : ", [measure.name for measure in empiricalModel.measures], '}'
            print >> f, '# Measure table'
            tableStr = '{'
            firstRow = True
            for prob in sorted(empiricalModel.measure_value_table.get_problems()):
                if firstRow :
                    tableStr = tableStr + "'" + prob + "' : "
                    firstRow = False
                else:
                    tableStr = tableStr + ',\n' + "'" + prob + "' : "
                tableStr = tableStr + str(empiricalModel.measure_value_table.get_row(prob))
            tableStr = tableStr + '}'
            print >> f, tableStr
        f.close()
        return
        
'''

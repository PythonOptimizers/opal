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
    
    def __init__(self, name=None, handlers=[]):
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
        self.logger.log(level, message)
        return


class Debugger:
    def __init__(self, fileName='opal-debug.log'):
        self.logger = logging.getLogger('DEBUG')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename=fileName)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(\
            '%(asctime)s - %(name)s:  %(message)s'))
        self.logger.addHandler(handler)
        return

    def log(self, message, level=logging.DEBUG):
        self.logger.log(level, message)
        return

debugger = Debugger()

    

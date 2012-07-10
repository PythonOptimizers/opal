"""

This module contains the fundmental description of a multi-agent systems.
It has three elements: agent, message and environment.

OPAL bases on a very simple multi-agent system in which each agent represents 
for an activity, a functionality. The agents communicate to cooperate by the 
message. The environment provide two basic serives: agent-location service 
and message transport service. 

The interaction of the agent is simple through the environment. There is no 
direct communication between two agents. Instead, the agent send its request, 
signal, reply to environment and choose suitable request from the environment. 

Language of communication is so simple within some type of messages such as 
request data, stop signal, wait signal ...

An multiagent-based application is activated by initializing an environment and
the concerned agents. After that, at least one event is raised to provoke the 
interaction between the agents.
"""

import hashlib
import threading
import log
import re

class Message:
    '''

    The Message class represent for communication among the agent.
    We base on the FIPA ACL Message Structure Specification 
    (http://www.fipa.org/specs/fipa00061/SC00061G.html#_Toc26669702)
    '''
    def __init__(self, 
                 performative='inform', 
                 sender=None, 
                 receiver=None,
                 reference=None, 
                 content=None,
                 language='python'):
        # Each message has an id assigned by the environment each time 
        # the message is posted (sent) by an agent
        self.id = None
        # See detail about FIPA Communicative Act Library Specification
        # (http://www.fipa.org/specs/fipa00037/SC00037J.html#_Toc26729689)
        # to understand performative
        self.performative = performative 
        # Participant of the message
        self.sender = sender
        self.receiver = None
        self.reference = reference
        self.content = content
        self.language = language
        return

    def serialize(self):
        """
        
        Return a string representing the message. This string is used 
        in message transfering or message delivering 
        """
        return ''

    def deserialize(self, messageStr):
        """
        
        Fill the fields from a message
        """
        return

class Agent(threading.Thread):
    """

    An Agent object represent for an activity, a functionality.

    A basic agent has some administrative methods:
    
    1. Register it to an environment
    2. Fetch the messages that work as a filter. Instead of getting all 
       messages posted to the environment, it chooses the suitable messages.   
    3. Decrypt a message to get information from the message content
    4. Encrypt a message to sent to environment
    5. Send message

    The life time of an agent is a loop that comsists the following activities
    

    I - Handle the messages
        1. Fetch messages
        2. Handle messages
           i) Decrypt message
           ii) Perform its manin activity.
           iii) (Optional) Reply   

    II - Send a request
        1. Ecrypt 

    """

    def __init__ (self, name='agent', logHandlers=[]):
        # At the moment of creation, the agent has no environment, this 
        # information is completed after its registration. The environment 
        # is the source and destination for the message of each agent.
        
        threading.Thread.__init__(self)
        self.id = None  # An identity is assigned only the agent is registered 
                        # to an environment
        self.environment = None  
        self.name = name
        self.working = True
        # Message handling of an agent is specified by 
        # set of handlers that are distinguished by command
        # Normally, a command is consist of message performative, 
        # and content expression (action expression) of message
        # For example, by default an agent has a handler that 
        # responds to stop working request from environment.
        self.message_handlers = {}
        # To prevent handle twice a message, the id of handled messages
        # is stored
        self.handled_messages = []
        # Each agent can define some parsers that parse the message content
        # basing on its content language. By default, the language is python
        # and the info obtained by function `eval`.
        self.content_parsers = {}
        self.logger = log.OPALLogger(name=name, handlers=logHandlers)
        # Each agent has some "timing" variables for synchronizing to the
        # environment. For example, to avoid to fetch a message one more time,
        # each agent use an integer variable to store the id of last message
        # examined in the previous fetching. 
        self.last_examined_message_id = 0
        return
    
    def send_message(self, msg):
        # If destination is not provided, the message will be distributed to 
        # to all environment that  the agnet belongs to
        if self.environment is None:
            return
        id = self.environment.message_service.add(msg)
        msg.id = id
        return

    def withdraw_message(self, messageId):
        if self.environment is None:
            return None
        self.environment.message_service.remove(messageId)
        return

    def fetch_messages(self):
        """
        
        A sub-class of Agent class rewrite this method to filter the messages 
        that it can handle. At least it won't catch the messages that it 
        posted.
        """

        if self.environment is None:
            return []
        # Fetch all message that receiver is agent or whose receiver is not 
        # specified
        #msgNum = self.environment.message_service.__len__()
        ## pattern = 'None|' + str(self.id)
        ## (queryResult, lastExamined) = self.environment.message_service.search(
        ##     beginPos=self.last_examined_message_id,
        ##     receiver=pattern)
        ## self.last_examined_message_id = lastExamined
        #for msg in queryResult:
        #    self.logger.log('Fetch message with id ' + str(msg.id))
        result = []
        ## for msg in queryResult:
        ##     if msg.id not in self.handled_messages and\
        ##            msg.sender is not self.id:
        ##         result.append(msg)
        messageBoxes = self.environment.message_service.message_boxes[self.id]
        while len(messageBoxes):
            result.append(messageBoxes.pop())
        return result


    def handle_message(self, message):
        '''
        
        The basic message handle is process stop request. This request say the 
        agent stop its work. The agent can react or not this request. By 
        default is turn working flag to False
        '''
        self.handled_messages.append(message.id)
        cmd, info = self.parse_message(message)
        if cmd is None: # The message could not be parsed
            self.logger.log('The message with id = ' + str(message.id) + \
                            ' could not be parsed')
            return

        if cmd in self.message_handlers.keys():
            self.logger.log('The message with id = ' + str(message.id) + \
                            ' interpreted as command: ' + cmd + \
                            ' with info: ' + str(info))
            self.message_handlers[cmd](info)
        return

    def parse_message(self, message):
        '''

        This method try to get neccessary information from the message
        by the suitable way. This means that with the same message, two agents
        can get different information.
    
        By default, the parsing procedure consists of two steps that return
        two things: the agent command and the message
        content in form of a set of content expression (action, proposition or
        identifying expression, see FIPA SL Content Language Specification 

        The command is extract first by forming a string from performative
        and the action.

        The information is get by apply the content parser corresponding to
        command. If content parser is specified, the whole content is
        transformed to a dictionary.  
        '''
        # Get command
        cmd = None
        # Check if this is a super message from environment
        # Process message from environment in a special way
        if message.sender is self.environment.id:
            self.logger.log('Receive a message from enviroment')
            cmd = str(self.environment.id)  + '-' + message.performative
        else:
            cmd = message.performative
       
        info = None
        # If there is a content parser corresponding to the message
        # performative, apply it
        if message.language in self.content_parsers.keys():
            info = (self.content_parsers[message.performative](message.content))
            # The obtained command is distingushed by peformative and 
            # information extracted from the content of message
        else: # Process by the default way
            try:
                if type(message.content) is type('a string'):
                    info = eval(message.content)
                else:
                    info = message.content
            except:
                info = None
        if info is not None:
            if 'action' in info.keys():
                cmd = cmd + '-' + info['action']
            elif ('proposition' in info.keys()) and \
                 ('what' in info['proposition'].keys()):
                cmd = cmd + '-' + info['proposition']['what']     
        return cmd, info
    
    def register(self, environment):
        
        """
        
        register to
        """
        self.id = environment.add_agent(self)
        # Set the pointer to registed environment
        self.environment = environment
        # Add environment name as prefix of the name
        self.name = environment.name + '.' + self.name
        # Handle message requesting stop working
        self.message_handlers[environment.id + '-request' + '-stop'] = self.stop
        #self.logger.log('I am registered with id = ' + self.id[0:4] + '...')
        return

    def unregister(self):
        self.environment.remove_agent(self.id)
      
        return
    
    def run(self):
        self.logger.log('I start my work')
        while self.working:
            # Fetch the messages
            messages = self.fetch_messages()
            # Handles the messages
            for msg in messages:
                self.handle_message(msg)
            # Delete the handled message
            del messages
        return

    # Message handlers

    def stop(self, info=None):
        '''
        
        Message handlers by default.
        '''
        self.working = False
        self.logger.log('I finish my work')
        return


class ManagementService:
    '''

    Represent for a management service. An environment need at least
    two root-services is message service that manages the message and 
    directory service that manages the agents.

    A management service has to has at least a storage and the administration 
    method like add, remove, modify and search.
    
    The common thing of the management services is the objects are 
    managed by id. Each object has an unique id provided when 
    adding to service.
    '''
    def __init__(self, name=None, logHandlers=[]):
        self.name = name
        self.managed_objects = {}
        self.logger = log.OPALLogger(name=name, handlers=logHandlers)
        return

    def create_id(self, obj):
        '''

        This function is overriden for each sub-class. It shows how the
        id of new object is generated. 
        '''
        return None

    def add(self, obj):
        id = self.create_id(obj)
        self.managed_objects[id] = obj
        return id 

    def remove(self, objId):
        if objId not in self.managed_objects:
            return
        del self.managed_objects[objId]
        return

    def __len__(self):
        return len(self.managed_objects)

    def get(self, id):
        try:
            return self.managed_objects[id]
        except:
            return None
        
    def search(self, query=None, **kwargs):
        if query is None:
            query = Query(kwargs)
        query.update(**kwargs)
        result = []
        for obj in self.managed_objects.values():
            if query.match(obj):
                result.append(obj)
        return result
    

class Query:
    def __init__(self, name='query', patterns=None, **kwargs):
        self.patterns = {}
        if patterns is not None:
            self.patterns.update(patterns)
        self.patterns.update(kwargs)
        return

    def update(self, **kwargs):
        self.patterns.update(kwargs)
        return

    def match(self, obj):
        # This method will be overriden by the sub-class
        return True
    
class MessageQuery(Query):
    def __init__(self, name='message-query', pattern=None, **kwargs):
        Query.__init__(self, name=name, pattern=pattern, **kwargs)
        return

    def match(self, msg):
        if len(self.patterns) == 0:  # An emtry query is understood we
                                     # will select all message
            return True
        if 'receiver' in self.patterns.keys() and  \
                re.match(self.patterns['receiver'], str(msg.receiver)):     
            return True
        return False

class MessageService(ManagementService):
    def __init__(self, logHandlers=[]):
        ManagementService.__init__(self, name='message service', 
                                   logHandlers=logHandlers)
        # message boxes store the messages for each agent. When
        # an agent registers to the environment, its messages box
        # is created. When a broadcast message is received, its
        # content will be delivered to all message box but the
        # sender. The elements in a message box is deleted by
        # the owner agent.
        self.message_boxes = {} 
        return

    def create_id(self, obj):
        #import time
        #id = time.time()
        # Creaating id following this way has potential problem if
        # message service has a deleting message feature
        id = self.__len__()
        return id

    def add(self, msg):
        id = ManagementService.add(self, msg)
        msg.id = id
        self.logger.log('Receive a ' + msg.performative + ' message' +\
                        ' from ' + str(msg.sender)[0:4] + '...' +\
                        ' assigned id as ' + str(msg.id) +\
                        ' with content ' + str(msg.content))
        # Now deliver the message to message boxes.
        # If it is not a broadcast message, deliver to corresponding message
        # box
        if msg.receiver is not None:
            if receiver in self.message_boxes.keys():
                self.message_boxes[receiver].append(msg)
        else: # If it is a broadcast, deliver copies to all message boxes but
            # sender
            for receiver in self.message_boxes.keys():
                if not (receiver == msg.sender):
                    self.message_boxes[receiver].append(msg)
        
        return id

    def search(self, query=None, beginPos=0, **kwargs):
        if query is None:
            query = MessageQuery(**kwargs)
        else:
            query.update(**kwargs)
        # Because the id also plays the role of ordering,
        # the searching in message service is modified a little
        # This method is called possibly with a argument indicating
        # the begin position of search. This to avoid the
        # research the old message (the handled message)
        endPos = self.__len__()
        #self.logger.log('Searching from ' + str(beginPos) + ' to ' +\
        #               str(endPos))
        result = []
        for pos in range(beginPos, endPos):
            msg = self.get(pos)
            #self.logger.log('Examine message' +\
            #                ' from ' + str(msg.sender)[0:4] + '...' +\
            #                ' assigned id as ' + str(msg.id) +\
            #                ' with content ' + str(msg.content))
            if (msg is not None) and query.match(msg):
                result.append(msg)
        return (result, endPos)
                
        
    
class DirectoryService(ManagementService):
    def __init__(self, logHandlers=[]):
        ManagementService.__init__(self, name='directory service', 
                                   logHandlers=logHandlers)
        return

    def create_id(self, agent):
        agentId = hashlib.sha1(agent.name).hexdigest()
        return agentId

    def get_all(self):
        return self.managed_objects.values()

class Environment(threading.Thread):
    """
    
    An Environment object is considered sometime as a special agent. It 
    provides two special services: agent locating and meage transporting
    
    The locating service is realized by just a list of agent. Because all 
    the agents are in a same machine, no more information is needed. Each 
    agent is assigned to an ID provided by the environment.

    The message transport serivce is simple too. It seems to be a billboard 
    for the agents post their messages. Only the agent who posts the message 
    can delete the message. Each message is distinguished by an ID and ID of 
    the sender.

    The most important and unique feature of an environment is creation of 
    agents, activate the agents and stop the agents. For an application, there 
    is only one environment is created.
    """

    def __init__(self, name='environment', logHandlers=[]):
        threading.Thread.__init__(self)
        self.id = hashlib.sha1(name).hexdigest()
        self.name = name
        self.message_service = MessageService()
        self.directory_service = DirectoryService() 
        self.logger = log.OPALLogger(name=name, handlers=logHandlers)
        return

    def initialize(self):
        # Activate all agent
        for agent in self.directory_service.get_all():
            agent.start()
        return

    def finalize(self):
        # Deacitavte all agent
        msg = Message(performative='request',
                      sender=self.id,
                      receiver=None,
                      reference=None,
                      content={'action':'stop'})
        self.message_service.add(msg)
        # Wait all agent finish there work
        for agent in self.directory_service.get_all():
            if agent.is_alive():
                self.logger.log('Waiting for ' + agent.name)
                agent.join()
        self.logger.log('Environment is shut down \n\n')
        return

    def add_agent(self, agent):
        # Add new agent and prepare everything for this new agent.
        # First of all, create an id for new agent add it to
        # directory service
        agentId = self.directory_service.add(agent)
        # Create an empty message box for new agent
        self.message_service.message_boxes[agentId] = []
        return agentId

    def remove_agent(self, agentId):
        self.directory_service.remove(agentId)
        self.message_service.message_boxes[agentId]
        return
    
    def run(self):
        return


    
    

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
import logging

class Message:
    def __init__(self, 
                 type=None, 
                 poster=None, 
                 reference=None, 
                 content=None):
        self.id = None
        self.type = type
        self.poster = poster
        self.reference = reference
        self.content = content

        return

    def serialize(self):
        """
        Return a string representing the message. This string is used 
        in message transfering or message delivering 
        """
        return 

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
        self.environments={}  # An agent can belong to one or many envivronment
                              # A belonging relation between an agent and an
                              # environment is an element (id:environ) of a dict 
                              # variable 
        self.name = name
        self.alive = True
        self.log_handlers = []
        self.log_handlers.extend(logHandlers)
    
        return

    def send_message(self, dest=None):
        # If destination is not provided, the message will be distributed to 
        # to all environment that  the agnet beloongs to
        return

    def fetch_messages(self):
        """
        
        A sub-class of Agent class rewrite this method to filter the messages 
        that it can handle. At least it won't catch the messages that it posted.
        
        """
        return []

    def decrypt_message(self, message):
        """

        A sub-class of Agent class rewrite this method to get neccessary 
        information from message content. The same message can give the 
        different information to different agents.
        """
        return
    
    def encrypt(self):
        return 
    
    def register(self, environment=None):
        
        """
        
        register to
        """
        id = environment.add_agent(self)
        self.environments[id] = environment
        return

    def run(self):
        while self.alive:
            messages = self.fetch_messages()
            for msg in messages:
                self.handle_message(msg)
        return

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

    An enviroment
    """

    def __init__(self, name='environment', logHandlers=[]):
        threading.Thread.__init__(self)
        self.name = name
        self.messages = []
        self.agents = {}
        self.activate_event = None
        self.log_handlers = []
        self.log_handlers.extend(logHandlers)
        return

    def initialize(self):
        return

    def finalize(self):
        return

    def add_message(self, message):
        return

    def remove_message(self, messageId, agentId):
        return

    def seach_message(self, query=None):
        return

    def run(self):
        return

    def add_agent(self, agent):
        id = hashlib.sha1(agent.name)
        self.agents[id] = agent 
        return id

    def remove_agent(self, id):
        return
    
    def search_agent(self, query):
        return

class Broker(Agent, Environment):
    def __init__(self, name='broker',logHandlers=[]):
        Agent.__init__(self, name=name, logHandlers=logHandlers)
        Environment.__init__(self)
        return


    def run(self):
        return
    
    
    

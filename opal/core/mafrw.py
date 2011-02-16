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

import threading

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
        return a string
        """
        return 

    def deserialize(self, messageStr):
        """
        
        Fill the fields from a message
        """
        return

class Agent(thread.Threading):
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

    def __init__ (self):
        # At the moment of creation, the agent has no environment, this 
        # information is completed after its registration. The environment 
        # is the source and destination for the message of each agent.
        self.environment=None
        return

    def fetch_messages(self):
        """
        
        A sub-class of Agent class rewrite this method to filter the messages 
        that it can handle. At least it won't catch the messages that it posted.
        
        """
        return

    def decrypt_message(self, message):
        """

        A sub-class of Agent class rewrite this method to get neccessary 
        information from message content. The same message can give the 
        different information to different agents.
        """
        return
    
    def encrypt(self):
        return 
    
    def register(self):
        
        """
        
        register to
        """
        return

class Environment(thread.Threading):
    """
    
    An Environment object is considered sometime as a special agent. It 
    provides two special services: agent locating and message transporting
    
    The locating service is realized by just a list of agent. Because all 
    the agents are in a same machine, no more information is needed. Each 
    agent is assigned to an ID provided by the environment.

    The message transport serivce is simple too. It seems to be a billboard 
    for the agents post their messages. Only the agent who posts the message 
    can delete the message. Each message is distinguished by an ID and ID of 
    the poster.
    """

    def __init__(self):
        self.messages = []
        self.agents = []
        return


    def add_message(self, message):
        return

    def remove_message(self, messageId, agentId):
        return

    def add_agent(self, agent):
        return
    
    
    

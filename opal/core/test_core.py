def test_multi_agent_framework():
    from mafrw import Agent
    from mafrw import Broker
    from mafrw import Environment

    agent = Agent()
    broker = Broker()
    env = Environment()
    
    broker.register(env)
    agent.register(broker)

    

def test_multi_agent_framework():
    from mafrw import Agent
    from mafrw import Environment

    agent = Agent()
    env = Environment()

    agent.register(env)




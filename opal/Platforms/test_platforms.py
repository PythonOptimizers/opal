def test_linux_platform():
    #assert 'b' == 'b'
    from ..core.mafrw import Environment
    from linux import LINUX

    env = Environment(name='test platform environment')
    LINUX.register(env)
    LINUX.submit('ls')


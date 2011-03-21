'''

This file for provoking a serie of tests relating all basic componnents 
in OPAL. It is used to provoke as well as the simple examples that are 
in the `examples` directory.

The `nose` package is required to run the tests.  

For testing OPAL installation, just launch at shell prompt a command:

  shell$ python test.py

For running a examples, for example the `finite-difference` examples:

  shell$ python test.py -w examples/fd
'''

if __name__ == '__main__':
    try: 
        from nose import main
        main()
    except NameError:
        print 'The NOSE package is required'

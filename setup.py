from distutils.core import setup

setup(name='ParOpt',
      version='0.1',
      description='Algorithmic Parameter Optimization',
      author='Charles Audet, Cong-Kien Dang, Dominique Orban',
      author_email='cong-kien.dang@polymtl.ca',
      url='http://www.gerad.ca/~kiendc',
      packages=['paropt',
                'paropt.core', 
                'paropt.Algorithms',
                'paropt.Measures',
                'paropt.Platforms',
                'paropt.Solvers',
                'paropt.TestProblemCollections']
     )


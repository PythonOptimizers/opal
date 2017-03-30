from distutils.core import setup

setup(name='OPAL - OPtimization of ALgorithm',
      version='1.3',
      description='Algorithmic Parameter Optimization',
      author='Charles Audet, Cong-Kien Dang, Dominique Orban',
      author_email='cong-kien.dang@polymtl.ca',
      url='http://www.gerad.ca/~kiendc/build/hmtl',
      packages=['opal',
                'opal.core',
                'opal.Platforms',
                'opal.Solvers',
                'opal.TestProblemCollections']
     )


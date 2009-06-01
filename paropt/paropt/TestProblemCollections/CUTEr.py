
import shutil
import os.path
import pickle
import sys
#from paropt.components.testenv import CUTEr as testEnvironment

from ..core.testproblem import *

from cuterfactory import CUTErFactory
from cuterfactory import Query

data_file = os.path.join(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)),'CUTEr.data')
#print data_file
# Object definition        
try:
    f = open(data_file,'r')
    CUTEr = pickle.load(f)
    f.close()
except IOError:
    CUTEr_factory = CUTErFactory(classifyFile=os.environ['MASTSIF'] + '/problem-classification.list')
    CUTEr =  ProblemCollection(name='CUTEr collection')
    HS = ProblemSet(name='Hock-Schittkowski test problems')
    for prob_name in CUTEr_factory.extract(name='HS\d+'):
        HS.add_problem(CUTEr_factory.generate_problem(prob_name))
    CUTEr.add_subcollection(HS)
    CUTEr.HS = HS
    f = open(data_file,'w')
    pickle.dump(CUTEr,f)
    f.close()


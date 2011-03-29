import shutil
import os.path
import pickle
import sys
#from paropt.components.testenv import CUTEr as testEnvironment

from ..core.testproblem import *

from cuterfactory import CUTErFactory
from cuterfactory import CUTErQuery

#data_file = os.path.join(os.path.dirname(os.path.abspath(sys.modules[__name__].__file__)),'CUTEr.data')
data_file = os.path.join(os.path.expanduser('~'),'.opal/CUTEr.data')
#print data_file
# Object definition
try:
    f = open(data_file,'r')
    CUTEr = pickle.load(f)
    f.close()
except IOError:
    classfDir = os.environ['MASTSIF']
    classfName='CLASSF.DB'  # Standard name for CUTEr classify file
    classfFile = os.path.join(classfDir, classfName)
    CUTEr_factory = CUTErFactory(classifyFile=classfFile)
    CUTEr = CUTEr_factory.generate_collection() 
    CUTEr.HS = CUTEr.select(CUTErQuery(name='HS\d+'))
    f = open(data_file,'w')
    pickle.dump(CUTEr,f)
    f.close()

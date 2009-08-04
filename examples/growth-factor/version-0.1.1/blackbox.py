#!/userdata/users/codan/local/python/bin/python
import os
import sys
import string
import shutil
import pickle
from dev.paropt.core import modeldata
from dev.paropt.core import blackbox
from dev.paropt.Solvers import NOMAD
# load the test data
try:
    blackboxDataFile = open("blackbox.dat","r")
    blackbox = pickle.load(blackboxDataFile)
    blackboxDataFile.close()
except TypeError:
    print "Error in loading"
blackbox.run(sys.argv)
try:
    blackboxDataFile = open("blackbox.dat","w")
    pickle.dump(blackbox,blackboxDataFile)
    blackboxDataFile.close()
except TypeError:
    print "Error in loading"

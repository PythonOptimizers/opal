import os
import sys
import string
import shutil
import pickle
from dev.opal.core import modeldata
from dev.opal.core import blackbox
from dev.opal.Solvers import NOMAD
# load the test data
try:
    blackboxDataFile = open("blackbox.dat","r")
    blackbox = pickle.load(blackboxDataFile)
    blackboxDataFile.close()
except TypeError:
    print "Error in loading"
blackbox.run(sys.argv)
blackbox.save()

import os
import sys
import string
import shutil
import pickle
from dev.opal.core import modeldata
from dev.opal.core import blackbox
# load the test data
try:
    blackboxDataFile = open("test_uncons_bb-1-9.dat","r")
    blackbox = pickle.load(blackboxDataFile)
    blackboxDataFile.close()
except TypeError:
    print "Error in loading"
blackbox.run(sys.argv)
blackbox.save()

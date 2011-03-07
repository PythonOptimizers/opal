from lsf import LSF
from linux import LINUX
from mpi import OPALMPI
from smp import SMP

supported_platforms = {'LINUX': LINUX,
                       'LSF': LSF,
                       'SMP': SMP}

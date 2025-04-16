from unittest import TestCase
from sys import platform
from hybridio.logging.logger import *


#TODO: now computer-specific, resolve!
if platform == "linux" or platform == "linux2":
    # linux
    path = "unknown"
elif platform == "darwin":
    # OS X
    path = "/Users/bvanacker/Documents/00_Development/02_Projects/00_Ongoing/DEME_PHASE2/01_RemoteRepositories/rpio-core/rpio/logging/tests/input/Project1"
elif platform == "win32":
    # Windows...
    path = "C:/Users/Bert/Private/99_RemoteRepositories/HybridIO/hybridio-core/hybridio/logging/tests/input/Project1"



class testLogger(TestCase):
    def setup(self):
        self.assertTrue(True)

    def test_initialization(self):
        logger = Logger(name="Custom logger",path=path,verbose=True)
        logger.syslog(msg="this is a test message")
        #CHECKS
        self.assertTrue(logger.name,"Custom logger")











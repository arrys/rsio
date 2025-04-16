from unittest import TestCase
from rpio.package.manager import *



class testPackageManager(TestCase):
    def setup(self):
        self.assertTrue(True)

    def test_initialization(self):
        manager = PackageManager(name="robosapiens IO package manager", verbose=True)

        #CHECKS
        self.assertTrue(manager.name,"robosapiens IO package manager")
        self.assertTrue(manager.description,'Build-in package manager')

    def test_pkgCreate(self):
        manager = PackageManager(name="robosapiens IO package manager", verbose=True)

        # -- create package --
        manager.create(name="Project1",standalone=True,path="output")

        # CHECKS
        self.assertTrue(manager.name, "robosapiens IO package manager")
        self.assertTrue(manager.description, 'Build-in package manager')

    def test_pkgCheck(self):
        manager = PackageManager(name="robosapiens IO package manager", verbose=True)

        # -- check package --
        isValidPkg = manager.check("input/reference_pkg")


        # CHECKS
        self.assertTrue(manager.name, "robosapiens IO package manager")
        self.assertTrue(manager.description, 'Build-in package manager')
        self.assertTrue(isValidPkg, True)










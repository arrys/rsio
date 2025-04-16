from rpio.package.manager import *

m = PackageManager(verbose=True)
m.create(name="HelloWorld_v2", standalone=True, path=None)
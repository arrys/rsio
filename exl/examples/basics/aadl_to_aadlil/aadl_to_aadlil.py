#**********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.parsers.parsers import *
from rpio.metamodels.aadl2_IL import *

# 1. Setup the AADL parser
parser = AADL_parser(logicalArchitecture='input/logicalArchitecture.aadl',physicalArchitecture='input/PhysicalArchitecture.aadl',messages='input/messages.aadl')

# 2. parse the aadl models and store in AADLIL
s = parser.aadl2aadlIl()
# 3. dump to aadlil json
s.object2json(fileName='output/system.json')
# 3. reload the AADLIL from json
loadedSystem = system(name="adaptiveSystem", description="Generated from AADL models",JSONDescriptor='output/system.json')
loadedSystem.object2json(fileName='output/loaded.json')

#**********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.metamodels.aadl2_IL import *

# 1. Load design from AADLIL model
loadedSystem = system(name="adaptiveSystem", description="Loaded from aadlil",JSONDescriptor='input/design.json')
x = 1


#**********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.parsers.parsers import *
from rpio.transformations.transformations import robochart2aadlmessages


# 1. Setup the robochart parser
parser = RobochartParser(maplek='input/MAPLE-K.rct', monitor='input/Monitor.rct', analysis='input/Analysis.rct', plan='input/Plan.rct', legitimate='input/Legitimate.rct', execute='input/Execute.rct', knowledge='input/Knowledge.rct')

# 2. Generate AADL models
x = robochart2aadlmessages(maplek=parser.maplek_model,path='output/')

x=1

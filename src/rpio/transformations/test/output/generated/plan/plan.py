# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.clientLibraries.rpclpy.node import Node
from ...Messages.messages import *


class plan(Node):

    def __init__(self, config='config.yaml',verbose=False):
        super().__init__(config=config,verbose=verbose)

        self._name = "plan"
        self.logger.log("plan instantiated")


    # -----------------------------AUTO-GEN SKELETON FOR planner-----------------------------
    def planner(self):

        #TODO: ADD USER CODE FOR planner


        knowledge = predictedPath()
        knowledge._Confidence= "SET VALUE"    # datatype: Float_64
        knowledge._Waypoints= "SET VALUE"    # datatype: Float_32
        _success = self.knowledge.write(cls=knowledge)

        self.eventHandler.send(eventName='plan')    # LINK <outport> plan



    def register_callbacks(self):

def main(args=None):

    node = plan()
    node.register_callbacks()
    node.start()

if __name__ == '__main__':
    main()
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


class monitor(Node):

    def __init__(self, config='config.yaml',verbose=False):
        super().__init__(config=config,verbose=verbose)

        self._name = "monitor"
        self.logger.log("monitor instantiated")


    # -----------------------------AUTO-GEN SKELETON FOR shipPoseEstimation-----------------------------
    def shipPoseEstimation(self):
        weatherConditions = self.knowledge.read("weatherConditions",queueSize=1)
        shipPose = self.knowledge.read("shipPose",queueSize=1)
        shipAction = self.knowledge.read("shipAction",queueSize=1)

        #TODO: ADD USER CODE FOR shipPoseEstimation


        knowledge = predictedPath()
        knowledge._Confidence= "SET VALUE"    # datatype: Float_64
        knowledge._Waypoints= "SET VALUE"    # datatype: Float_32
        _success = self.knowledge.write(cls=knowledge)

        self.eventHandler.send(eventName='pathEstimate')    # LINK <outport> pathEstimate



    def register_callbacks(self):
        self.eventHandler.subscribe(eventName='newData', function=self.shipPoseEstimation)     # LINK <eventTrigger> newData
        self.eventHandler.subscribe(eventName='weatherConditions', function=self.shipPoseEstimation)        # LINK <inport> weatherConditions
        self.eventHandler.subscribe(eventName='shipPose', function=self.shipPoseEstimation)        # LINK <inport> shipPose
        self.eventHandler.subscribe(eventName='shipAction', function=self.shipPoseEstimation)        # LINK <inport> shipAction

def main(args=None):

    node = monitor()
    node.register_callbacks()
    node.start()

if __name__ == '__main__':
    main()
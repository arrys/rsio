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


class execute(Node):

    def __init__(self, config='config.yaml',verbose=False):
        super().__init__(config=config,verbose=verbose)

        self._name = "execute"
        self.logger.log("execute instantiated")


    # -----------------------------AUTO-GEN SKELETON FOR executer-----------------------------
    def executer(self):
        plan = self.knowledge.read("plan",queueSize=1)
        isLegit = self.knowledge.read("isLegit",queueSize=1)

        #TODO: ADD USER CODE FOR executer


        knowledge = predictedPath()
        knowledge._Confidence= "SET VALUE"    # datatype: Float_64
        knowledge._Waypoints= "SET VALUE"    # datatype: Float_32
        _success = self.knowledge.write(cls=knowledge)

        self.eventHandler.send(eventName='pathEstimate')    # LINK <outport> pathEstimate



    def register_callbacks(self):
        self.eventHandler.subscribe(eventName='plan', function=self.executer)        # LINK <inport> plan
        self.eventHandler.subscribe(eventName='isLegit', function=self.executer)        # LINK <inport> isLegit

def main(args=None):

    node = execute()
    node.register_callbacks()
    node.start()

if __name__ == '__main__':
    main()
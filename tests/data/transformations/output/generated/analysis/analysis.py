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


class analysis(Node):

    def __init__(self, config='config.yaml',verbose=False):
        super().__init__(config=config,verbose=verbose)

        self._name = "analysis"
        self.logger.log("analysis instantiated")


    # -----------------------------AUTO-GEN SKELETON FOR analyzePathPredictions-----------------------------
    def analyzePathPredictions(self):
        pathEstimate = self.knowledge.read("pathEstimate",queueSize=1)

        #TODO: ADD USER CODE FOR analyzePathPredictions


        knowledge = AnomalyMessage()
        knowledge._Anomaly= "SET VALUE"    # datatype: Boolean
        _success = self.knowledge.write(cls=knowledge)

        self.eventHandler.send(eventName='pathAnomaly')    # LINK <outport> pathAnomaly



    def register_callbacks(self):
        self.eventHandler.subscribe(eventName='anomaly', function=self.analyzePathPredictions)     # LINK <eventTrigger> anomaly

def main(args=None):

    node = analysis()
    node.register_callbacks()
    node.start()

if __name__ == '__main__':
    main()
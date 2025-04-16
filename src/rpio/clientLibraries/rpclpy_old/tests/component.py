# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from rpio.clientLibraries.rpclpy.node import Node
from messages import *


class monitor(Node):

    def __init__(self, config='config.yaml',verbose=True):
        super().__init__(config=config,verbose=verbose)

        self._name = "monitor"
        self.logger.log("TESTING THE LOGGER OF THE MQTT NODE")

        #read knowledge
        weatherConditions = self.knowledge.read("weatherConditions", queueSize=1)

        #try to send a knowledge element
        knowledge = predictedPath()
        knowledge._Confidence = 1 # datatype: Float_64
        knowledge._Waypoints = 45  # datatype: Float_32
        _success = self.knowledge.write(cls=knowledge)

        #register incoming events and triggers
        self.eventHandler.send(eventName='event1')

    def register_callbacks(self):
        self.eventHandler.subscribe(eventName='event2', function=self.function1)
        self.eventHandler.subscribe(eventName='event3', function=self.function2)
        #self.register_event_callback(eventName='event3', function=self.function2)

    def function1(self):
        print("Function 1 triggered from event2")

    def function2(self):
        print("Function 2 triggered from event3")

def main(args=None):

    node = monitor()
    node.register_callbacks()
    node.start()

if __name__ == '__main__':
    main()


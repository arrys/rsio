# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from RoboSapiensAdaptivePlatform.utils.nodes import TriggeredNode
from RoboSapiensAdaptivePlatform.Communication.Messages.messages import ComponentStatus
from RoboSapiensAdaptivePlatform.utils.constants import *



class monitor(TriggeredNode):

    def __init__(self, logger = None,knowledgeBase = None,verbose=False):
        super().__init__(logger=logger,knowledge = knowledgeBase,verbose=verbose)

        self._name = "monitor"

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def _SpinOnceFcn(self, args):

        # 1. FETCH KNOWLEDGE FROM KNOWLEDGE BASE VIA KNOWLEGE MANAGEMENT
        p1,history1 = self.knowledge.read("temperature_average",queueSize=10)

        # 2. PERFORM MONITORING
        #!!--------------DUMMY---------------!!
        average = sum(history1) / len(history1)
        if average<40:
            _status = monitorStatus.ANOMALY
            _accuracy = 0.95
        elif average>45:
            _status = monitorStatus.ANOMALY
            _accuracy = 0.91
        else:
            _status = monitorStatus.NORMAL
            _accuracy = 1.0
        #!!--------------DUMMY - --------------!!

        # 3. SIGNAL MONITORING STATE VIA KNOWLEDGE
        self.RaPSignalStatus(component=adaptivityComponents.MONITOR,status=_status,accuracy=_accuracy)


        self.logger.log("["+self._name+"] - "+"Monitoring property: "+p1.name +" with values:"+history1.__str__())

        # 4. return status of execution (fail = False, success = True)
        return True

    def _EnterInitializationModeFcn(self):
        if self._verbose: print("["+self._name+"] - "+"Enter initializationModeFcn not implemented")

    def _ExitInitializationModeFcn(self):
        # initial signal after startup
        self.RaPSignalStatus(component=adaptivityComponents.MONITOR,status=monitorStatus.NORMAL,accuracy=1.0)

    def _EnterConfigurationModeFcn(self):
        if self._verbose: print("["+self._name+"] - "+"Enter configurationModeFcn not implemented")


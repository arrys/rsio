# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from RoboSapiensAdaptivePlatform.utils.constants import *
from RoboSapiensAdaptivePlatform.utils.timer import perpetualTimer
from RoboSapiensAdaptivePlatform.ManagedSystem.ManagedSystemTemplates import localManagedSystem


class managedSystem(localManagedSystem):

    def __init__(self,name = "Local managed system Templates",description = "A local managed system Templates for RaP.",logger=None,effector = None,probe=None,verbose=False):
        super().__init__(name = name,description = description,logger=logger,effector = effector,probe=probe,verbose=verbose)

        # ADAPTABLE PARAMETERS/PROPERTIES
        self._light = 0
        self._temperature_average = 42.0
        self._LidOpenTicks = 5  # after Xs lid opens
        self._counter = 0

        # --- Overload the effector spin function if RaP is passed ---
        self._RaPEffector.RaPSpin_once = self._effector_spin_once

        # --- System simulation stepping and periodic probing of the system ---
        self._dt = 0.5
        self._probe_executor = perpetualTimer(self._dt, self._probes_update)
        self._systemStep_executor = perpetualTimer(self._dt, self._systemStep)

        # --- Auto-start system simulation and probing executor ---
        self._systemStep_executor.start()
        self._probe_executor.start()

    def _systemStep(self):

        # DUMMY SYSTEM BEHAVIOR
        # 1. hotbox closed, light off, opens after _LidOpenTicks, temperature drops (=anomaly1)
        # 2. hotbox open, light on, temperature increases, above max. temperature (=anomaly2)

        self._counter = self._counter + 1

        if self._counter <= self._LidOpenTicks:
            self._temperature_average = 42.0
        elif self._counter > self._LidOpenTicks and self._light != 1:
            self._temperature_average = self._temperature_average - 1
        elif self._counter > self._LidOpenTicks and self._light != 0:
            self._temperature_average = self._temperature_average + 0.5
        else:
            self._counter = 0

    def _probes_update(self):
        #probe light parameters
        self.RaPProbe.push('light',self._light)
        self.RaPProbe.push('temperature_average',self._temperature_average)

    def _effector_spin_once(self,action):
        _status = effectorStatus.IDLE

        # 1. DECODE THE ACTION TO BE PERFORMED
        _rawAction = action
        _actionType = _rawAction.ID
        _description = _rawAction.description
        _propertyList = _rawAction.propertyList

        if _actionType == actionType.DIAGNOSISTYPE:
            # 2a. PERFORM THE DIAGNOSE ACTION ROUTINE
            self.RaPLogger.log("["+self._name+"] - "+'Managed system diagnose - "' + _description + '"')
            _status = effectorStatus.DIAGNOSIS

            # ----------------- USER SPECIFIC ADAPTATION CODE ------------------
            # PERFORM PRE-ACTIONS, e.g., safestate

            # CHANGE ALL PROPERTIES

            # PERFORM POST-ACTIONS, e.g. startup
            # --------------------------------------------------------------------

        elif _actionType == actionType.ADAPTATIONTYPE:
            # 2b. PERFORM THE ADAPTATION ACTION ROUTINE
            self.RaPLogger.log("["+self._name+"] - "+'Managed system adaptation - "' + _description + '"')
            _status = effectorStatus.ADAPTATION

            # ----------------- USER SPECIFIC ADAPTATION CODE ------------------
            # PERFORM PRE-ACTIONS, e.g., safestate

            # CHANGE ALL PROPERTIES
            for p in _propertyList:
                try:
                    old = getattr(self, "_"+p.name,)
                    setattr(self, "_"+p.name, p.value)
                    self.RaPLogger.log("["+self._name+"] - "+'SUCCESS - ADAPTED property "' + p.name + '" from value "' + old.__str__() + '" to value "' + p.value.__str__()+ '"' )
                except:
                    self.RaPLogger.log("["+self._name+"] - "+'ERROR - FAILED TO ADAPT property "' + p.name)

            # PERFORM POST-ACTIONS, e.g. startup

            #--------------------------------------------------------------------


        else:
            self.RaPLogger.log("ERROR - Unknown action type")

        # 3. RETURN STATUS OF THE ACTION
        return _status




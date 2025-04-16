from rpio.clientLibraries.rpclpy.constants import *
from rpio.clientLibraries.rpclpy.remote.mqtt.rx_utils import Logger, Knowledge, EventHandler

class Node(object):

    def __init__(self,config='00_input/config.yaml',verbose=False):

        self._name = "Generic Node"
        self._description = "Generic node used within RoboSapiens Adaptive Platform."
        self._verbose = verbose
        self._state = genericNodeStates.INSTANTIATED
        # RoboSapiens Adaptive Platform elements

        self._RaPKnowledge = Knowledge(config=config,verbose=verbose)
        self._RaPlogger = Logger(config=config,verbose=verbose)
        self._RaPlEventHandler = EventHandler(config=config,verbose=verbose)


    @property
    def name(self):
        """The name property (read-only)."""
        return self._name

    @property
    def description(self):
        """The description property (read-only)."""
        return self._description

    @property
    def state(self):
        """The state property (read-only)."""
        return self._state

    @property
    def logger(self):
        """The logger component (read-only)."""
        return self._RaPlogger

    @property
    def knowledge(self):
        """The logger component (read-only)."""
        return self._RaPKnowledge

    @property
    def eventHandler(self):
        """The logger component (read-only)."""
        return self._RaPlEventHandler

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INTERFACE FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def start(self):
        """Start the node."""
        x=1
        #TODO: implement the starting behavior

    def RaPEnterInitializationMode(self):
        """Function to enter the initialization mode of a genericNode.

			:return: `True` if enter initialization mode was successful, `False` otherwise
			:rtype: bool
			"""
        try:
            self._EnterInitializationModeFcn()
            self._state = genericNodeStates.INITIALIZATION_MODE
            return True
        except:
            return False

    def RaPExitInitializationMode(self):
        """Function to exit the initialization mode of a genericNode.

			:return: `True` if exit initialization mode was successful, `False` otherwise
			:rtype: bool
			"""
        try:
            self._ExitInitializationModeFcn()
            self._state = genericNodeStates.INITIALIZED
            return True
        except:
            return False

    def RaPEnterConfigurationMode(self):
        """Function to enter the configuration mode of a genericNode.

			:return: `True` if enter configuration mode was successful, `False` otherwise
			:rtype: bool
			"""
        try:
            self._state = genericNodeStates.CONFIGURATION_MODE
            self._EnterConfigurationModeFcn()
            return True
        except:
            self._state = genericNodeStates.INSTANTIATED
            return False

    def RaPExitConfigurationMode(self):
        """Function to exit the configuration mode of a genericNode.

		:return: `True` if exit configuration mode was successful, `False` otherwise
		:rtype: bool
		"""
        try:
            self._ExitConfigurationModeFcn()
            self._state = genericNodeStates.INSTANTIATED
            return True
        except:
            return False

    def RaPTerminate(self):
        """Function to terminate a genericNode.

			:return: `True` if node termination was successful, `False` otherwise
			:rtype: bool
			"""
        try:
            self._TerminateFcn()
            self._state = genericNodeStates.TERMINATED
            return True
        except:
            return False

    def RaPFreeInstance(self):
        """Function to terminate a genericNode.
			"""
        try:
            self._DestroyFcn()
            self._state = genericNodeStates.TERMINATED
            return True
        except:
            return False

    def RaPReset(self):
        """Function to reset a genericNode.
			"""
        try:
            self._ResetFcn()
            self._state = genericNodeStates.INSTANTIATED
            return True
        except:
            return False

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def _EnterInitializationModeFcn(self):
        if self._verbose: print("Enter initialization mode function call not implemented")

    def _ExitInitializationModeFcn(self):
        if self._verbose: print("Exit initialization mode function call not implemented")

    def _EnterConfigurationModeFcn(self):
        if self._verbose: print("Enter configuration mode function call not implemented")

    def _ExitConfigurationModeFcn(self):
        if self._verbose: print("Exit configuration mode function call not implemented")

    def _TerminateFcn(self):
        if self._verbose: print("Terminate function call not implemented")

    def _DestroyFcn(self):
        if self._verbose: print("Destroy function call not implemented")

    def _ResetFcn(self):
        if self._verbose: print("Reset function call not implemented")

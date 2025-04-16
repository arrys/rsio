import jsonpickle
import yaml

from rpio.clientLibraries.rpclpy.remote.mqtt.MQTTInterface import *
from rpio.clientLibraries.rpclpy.constants import *
from rpio.clientLibraries.rpclpy.utils import *

class Logger():

    def __init__(self, config="default",verbose=False):

        self._verbose = verbose
        # configurion file
        self._cfg = config

        # setup MQTT publisher
        self._publisher = None
        self._publishList = []

        # AUTO-CONFIG
        self.EnterConfigurationMode()
        self.ExitConfigurationMode()
        self.EnterInitializationMode()
        self.ExitInitializationMode()

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------EXTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def log(self,msg):
        if len(self._publishList) > 0:
            messageClass = LogMessage(name=self._publishList[0]["name"],message=msg)
            message = self._encode(message=messageClass)
            self._publisher.push(topic=self._publishList[0]["topic"], value=message)
        else:
            if self._verbose:print("ERROR - No logging publisher registered")

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def _encode(self,message):
        return jsonpickle.encode(message)

    def _create_publisher(self,cls=None,name="",topic='topic',QoS=10):
        self._publishList.append({'name': name, 'class': cls, 'topic': topic})

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INSTANTIATION FUNCTIONS------------------------------------
    # ------------------------------------------------------------------------------------------------

    def EnterInitializationMode(self):
        self._publisher = MQTTInterface(name="MQTTPublisher", VERBOSE=self._verbose)

    def ExitInitializationMode(self):
        self._publisher._mqttClient = self._publisher._mqtt_setup()
        self._publisher.start()

    def EnterConfigurationMode(self):
        with open(self._cfg, 'r') as file:
            cfg = yaml.safe_load(file)
            try:
                for msg in cfg["logger"]["endpoints"]:
                    p = msg["endpoint"]
                    self._create_publisher(cls=p["class"], name=p["name"], topic=p["topic"],QoS=p["QoS"])
            except:
                if self._verbose:print("ERROR - No logging endpoint registered")

    def ExitConfigurationMode(self):
        if self._verbose:print("ExitConfigurationMode not implemented")

class Knowledge():

    def __init__(self, config="default",verbose=False):

        self._verbose = verbose
        # configurion file
        self._cfg = config

        # setup MQTT publisher
        self._publisher = None
        self._publishList = []

        # setup MQTT subscriber
        self._subscriber = None
        self._subscriptionList = []
        self._subscriptionListTopics = []

        # AUTO-CONFIG
        self.EnterConfigurationMode()
        self.ExitConfigurationMode()
        self.EnterInitializationMode()
        self.ExitInitializationMode()

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------EXTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def read(self,name='',queueSize=1):
        x=1
        #TODO: implement a blocking read -> register a read request on 1 topic and wait for the reply

    def write(self,cls):
        if len(self._publishList) > 0:
            for publisher in self._publishList:
                if cls.name == publisher["name"]:
                    message = self._encode(message=cls)
                    self._publisher.push(topic=publisher["topic"], value=message)
        else:
            if self._verbose:print("ERROR - No logging publisher registered")

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def _encode(self,message):
        return jsonpickle.encode(message)

    def _create_publisher(self,cls=None,name="",topic='topic',QoS=10):
        self._publishList.append({'name': name, 'class': cls, 'topic': topic})

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INSTANTIATION FUNCTIONS------------------------------------
    # ------------------------------------------------------------------------------------------------

    def EnterInitializationMode(self):
        self._publisher = MQTTInterface(name="MQTTPublisher", VERBOSE=self._verbose)

    def ExitInitializationMode(self):
        self._publisher._mqttClient = self._publisher._mqtt_setup()
        self._publisher.start()
        #TODO: instantiate and start the subscriber

    def EnterConfigurationMode(self):
        with open(self._cfg, 'r') as file:
            cfg = yaml.safe_load(file)
            try:
                for msg in cfg["knowledgeOut"]["properties"]:
                    p = msg["property"]
                    self._create_publisher(cls=p["class"], name=p["name"], topic=p["topic"],QoS=p["QoS"])
                #TODO:configure the subscribers
            except:
                if self._verbose:print("WARNING: No Knowledge Out properties found")

    def ExitConfigurationMode(self):
        if self._verbose:print("ExitConfigurationMode not implemented")


class EventHandler():

    def __init__(self, config="default",verbose=False):

        self._verbose = verbose
        # configurion file
        self._cfg = config

        # setup MQTT publisher
        self._publisher = None
        self._publishList = []
        self._eventList = []

        # setup MQTT subscriber
        self._subscriber = None
        self._subscriptionList = []
        self._subscriptionListTopics = []

        # AUTO-CONFIG
        self.EnterConfigurationMode()
        self.ExitConfigurationMode()
        self.EnterInitializationMode()
        self.ExitInitializationMode()

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------EXTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def send(self,eventName):
        if len(self._publishList) > 0:
            for event in self._publishList:
                if eventName == event["name"]:
                    message = self._encode(message='event trigger')
                    self._publisher.push(topic=event["topic"], value=message)


    def subscribe(self,eventName,function):
        for event in self._subscriptionList:
            if eventName == event["name"]:
                event['function'] = function
    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INTERNAL FUNCTIONS----------------------------------------
    # ------------------------------------------------------------------------------------------------
    def _encode(self,message):
        return jsonpickle.encode(message)

    def _create_publisher(self,cls=None,name="",topic='topic',QoS=10):
        self._publishList.append({'name': name, 'class': cls, 'topic': topic})

    def _create_subscription(self,cls=None,name="",topic='topic',QoS=10):
        self._subscriptionList.append({'name': name, 'class': cls, 'topic': topic,'function':None})
        self._subscriptionListTopics.append(topic)

    def _messageReceiveCallback(self,args):
        msg = args
        for event in self._subscriptionList:
            if event["topic"] == msg.topic:
                event['function']() #call the corresponding function

    # ------------------------------------------------------------------------------------------------
    # -------------------------------------INSTANTIATION FUNCTIONS------------------------------------
    # ------------------------------------------------------------------------------------------------

    def EnterInitializationMode(self):
        self._publisher = MQTTInterface(name="MQTTPublisher", VERBOSE=self._verbose)
        self._subscriber = MQTTInterface(name="MQTTSubscriber", subscriptions=self._subscriptionListTopics,VERBOSE=self._verbose)
        self._subscriber._reactiveInput = True
        self._subscriber._messageReceiveCallback = self._messageReceiveCallback


    def ExitInitializationMode(self):
        self._publisher._mqttClient = self._publisher._mqtt_setup()
        self._publisher.start()
        self._subscriber._mqttClient = self._subscriber._mqtt_setup()
        self._subscriber.start()

    def EnterConfigurationMode(self):
        with open(self._cfg, 'r') as file:
            cfg = yaml.safe_load(file)
            try:
                for msg in cfg["eventOut"]["properties"]:
                    p = msg["property"]
                    self._create_publisher(cls=p["class"], name=p["name"], topic=p["topic"],QoS=p["QoS"])
            except:
                if self._verbose: print("WARNING: No Event Out properties found")

            try:
                for msg in cfg["eventIn"]["properties"]:
                    p = msg["property"]
                    self._create_subscription(cls=p["class"], name=p["name"], topic=p["topic"], QoS=p["QoS"])
            except:
                if self._verbose: print("WARNING: No Event in properties found")

    def ExitConfigurationMode(self):
        if self._verbose:print("ExitConfigurationMode not implemented")
import json
from pathlib import Path


class NamedObject(object):

    def __init__(self, name="tbd", description="tbd", verbose=False):
        self._name = name
        self._description = description
        self._verbose = verbose

    @property
    def name(self):
        """The name property (read-only)."""
        return self._name

    @property
    def description(self):
        """The description property (read-only)."""
        return self._description


class Process(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, feature_list=None, thread_list=None, formalism="python", containerization=False):
        super().__init__(name=name, description=description, verbose=verbose)

        if feature_list is not None:
            self._feature_list = feature_list
        else:
            self._feature_list = []

        if thread_list is not None:
            self._thread_list = thread_list
        else:
            self._thread_list = []

        self._formalism = formalism
        self._containerization = containerization

    @property
    def features(self):
        return self._feature_list

    def add_feature(self, feature):
        """Add a feature to the system """
        self._feature_list.append(feature)

    @property
    def threads(self):
        return self._thread_list

    def add_thread(self, t):
        """Add a thread to the system """
        self._thread_list.append(t)

    @property
    def formalism(self):
        return self._formalism

    @formalism.setter
    def formalism(self, f):
        self._formalism = f

    @property
    def containerization(self):
        return self._containerization

    @containerization.setter
    def containerization(self, c):
        self._containerization = c


class Thread(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, feature_list=None, event_trigger=None):
        super().__init__(name=name, description=description, verbose=verbose)
        if feature_list is not None:
            self._feature_list = feature_list
        else:
            self._feature_list = []
        self._event_trigger = event_trigger

    @property
    def features(self):
        return self._feature_list

    def add_feature(self, feature):
        """Add a feature to the system """
        self._feature_list.append(feature)

    @property
    def event_trigger(self):
        return self._event_trigger


class Characteristic(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, value="", data_type="-"):
        super().__init__(name=name, description=description, verbose=verbose)

        self._value = value
        self._dataType = data_type


class Event(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)


class Mode(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, callback=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self._callback = callback

    @property
    def callback(self):
        """The callback property (read-only)."""
        return self._callback


class Transition(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, callback=None, source=None, destination=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self._source = source
        self._destination = destination
        self._callback = callback

    @property
    def source(self):
        """The source (read-only)."""
        return self._source

    @property
    def destination(self):
        """The source (read-only)."""
        return self._destination

    @property
    def callback(self):
        """The callback property (read-only)."""
        return self._callback


class Feature(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, feature_type="feature"):
        super().__init__(name=name, description=description, verbose=verbose)

        self._feature_type = feature_type

    @property
    def feature_type(self):
        return self._feature_type

    @feature_type.setter
    def feature_type(self, type):
        self._feature_type = type


class Port(Feature):

    def __init__(self, name="tbd", description="tbd", initial_value=1.0, value_reference=1, type="data", message=None, verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)
        self._feature_type = "port"
        self._initial_value = initial_value
        self._value_reference = value_reference
        self._type = type
        self._message = message

    @property
    def value(self):
        """The value property (read)."""
        return self._initial_value

    @value.setter
    def value(self, value):
        """The value property (write)."""
        self._initial_value = value

    @property
    def value_reference(self):
        """The valueReference property (read)."""
        return self._value_reference

    @value_reference.setter
    def value_reference(self, value):
        """The valueReference property (write)."""
        self._value_reference = value

    @property
    def type(self):
        """The type property (read-only)."""
        return self._type

    @property
    def message(self):
        """The message property"""
        return self._message


class InPort(Port):
    def __init__(self, name="tbd", description="tbd", initial_value=1.0, value_reference=1, type="data", verbose=False, message=None):
        super().__init__(name=name, description=description, verbose=verbose, initial_value=initial_value, value_reference=value_reference, type=type, message=message)
        self._feature_type = "inport"


class OutPort(Port):
    def __init__(self, name="tbd", description="tbd", initial_value=1.0, value_reference=1, type="data", verbose=False, message=None):
        super().__init__(name=name, description=description, verbose=verbose, initial_value=initial_value, value_reference=value_reference, type=type, message=message)
        self._feature_type = "outport"


class Connection(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, source=None, destination=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self._source = source
        self._destination = destination

    @property
    def source(self):
        """The source (read-only)."""
        return self._source

    @property
    def destination(self):
        """The source (read-only)."""
        return self._destination


class Message(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, feature_list=None):
        super().__init__(name=name, description=description, verbose=verbose)

        if feature_list is not None:
            self._feature_list = feature_list
        else:
            self._feature_list = []

    @property
    def features(self):
        return self._feature_list

    def add_feature(self, feature):
        """Add a feature to the system """
        self._feature_list.append(feature)


class Data(Feature):

    def __init__(self, name="tbd", description="tbd", data_type="Float_64", verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)

        self._data_type = data_type

    @property
    def data_type(self):
        return self._data_type


class Processor(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, feature_list=None, property_list=None, binding_list=None, ip="localhost"):
        super().__init__(name=name, description=description, verbose=verbose)

        if feature_list is not None:
            self._feature_list = feature_list
        else:
            self._feature_list = []
        if property_list is not None:
            self._property_list = property_list
        else:
            self._property_list = []
        if binding_list is not None:
            self._binding_list = binding_list
        else:
            self._binding_list = []
        self._ip = ip
        self.rap_backbone = False

    def add_feature(self, feature):
        """Add a feature to the system """
        self._feature_list.append(feature)

    def add_property(self, p):
        """Add a property to the system """
        self._property_list.append(p)

    def add_processor_binding(self, process):
        """Add a processor binding to the processor """
        self._binding_list.append(process)

    @property
    def processor_binding(self):
        return self._binding_list

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @property
    def runs_rap_backbone(self):
        return self.rap_backbone

    @runs_rap_backbone.setter
    def runs_rap_backbone(self, flag):
        self.rap_backbone = flag


class Memory(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, property_list=None):
        super().__init__(name=name, description=description, verbose=verbose)

        if property_list is not None:
            self._property_list = property_list
        else:
            self._property_list = []

    def add_property(self, p):
        """Add a property to the system """
        self._property_list.append(p)


class Bus(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, property_list=None):
        super().__init__(name=name, description=description, verbose=verbose)

        if property_list is not None:
            self._property_list = property_list
        else:
            self._property_list = []

        self._connection_list = []

    def add_property(self, p):
        """Add a property to the bus """
        self._property_list.append(p)

    def add_connection(self, p):
        """Add a connection to the bus """
        self._connection_list.append(p)


class System(NamedObject):

    def __init__(self, name="tbd", description="tbd", verbose=False, system_list=None, process_list=None, feature_list=None, message_list=None, processor_list=None, package="", prefix="", json_descriptor: Path | None = None):
        super().__init__(name=name, description=description, verbose=verbose)

        if feature_list is not None:
            self._feature_list = feature_list
        else:
            self._feature_list = []
        if system_list is not None:
            self._system_list = system_list
        else:
            self._system_list = []
        if process_list is not None:
            self._process_list = process_list
        else:
            self._process_list = []
        if message_list is not None:
            self._message_list = message_list
        else:
            self._message_list = []
        if processor_list is not None:
            self._processor_list = processor_list
        else:
            self._processor_list = []

        if json_descriptor is not None:
            self.json2object(json_descriptor=json_descriptor)

    def add_process(self, process):
        """Add a process to the process list """
        self._process_list.append(process)

    @property
    def processes(self):
        return self._process_list

    @property
    def systems(self):
        return self._system_list

    def add_system(self, system):
        """Add a system to the system list """
        self._system_list.append(system)

    def add_feature(self, feature):
        """Add a feature to the system """
        self._feature_list.append(feature)

    def add_message(self, message):
        """Add a process to the process list."""
        self._message_list.append(message)

    @property
    def messages(self):
        return self._message_list

    @messages.setter
    def messages(self, d):
        self._message_list = d

    def add_processor(self, processor):
        """Add a processor to the system list."""
        self._processor_list.append(processor)

    @property
    def processors(self):
        return self._processor_list

    def object2json(self, file_name: Path):
        """Generate a JSON file."""
        data = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        file_name.write_text(data, encoding="utf-8")

    def json2object(self, json_descriptor: Path = Path("system.json")):
        """
        Function to generate an AADLIL system from a JSON file.

        :param json_descriptor: Path to the JSON file for the AADLIL system
        """
        json_object = json.loads(json_descriptor.read_text())
        # --setup object--
        self._name = json_object["_name"]
        self._description = json_object["_description"]
        # -- load messages --
        for m in json_object["_messageList"]:
            features = []
            for d in m["_featureList"]:
                temp_d = Data(name=d["_name"], data_type=d["_dataType"])
                features.append(temp_d)
            temp_message = Message(name=m["_name"], feature_list=features)
            self.add_message(temp_message)
        # -- load systems and containing processes --
        for s in json_object["_systemList"]:
            temp_s = System(name=s["_name"], description=s["_description"])
            for p in s["_processList"]:
                temp_p = Process(name=p["_name"], description=p["_description"])
                features = []
                for f in p["_featureList"]:
                    _m = None
                    for m in self.messages:
                        if f["_message"] is not None:
                            if m.name == f["_message"]["_name"]:
                                _m = m
                    if f["_featureType"] == "inport":
                        temp_f = InPort(name=f["_name"], type=f["_type"], message=_m)
                    elif f["_featureType"] == "outport":
                        temp_f = OutPort(name=f["_name"], type=f["_type"], message=_m)
                    else:
                        temp_f = ""
                    temp_p.add_feature(temp_f)
                threads = []
                for t in p["_threadList"]:
                    tfeatures = []
                    for f in t["_featureList"]:
                        _m = None
                        for m in self.messages:
                            if f["_message"] is not None:
                                if m.name == f["_message"]["_name"]:
                                    _m = m
                        if f["_featureType"] == "inport":
                            temp_f = InPort(name=f["_name"], type=f["_type"], message=_m)
                        elif f["_featureType"] == "outport":
                            temp_f = OutPort(name=f["_name"], type=f["_type"], message=_m)
                        else:
                            temp_f = ""
                        tfeatures.append(temp_f)
                    temp_t = Thread(name=t["_name"], feature_list=tfeatures, event_trigger=t["_eventTrigger"])
                    temp_p.add_thread(temp_t)
                temp_p.formalism = p["_formalism"]
                temp_p.containerization = p["_containerization"]
                temp_s.add_process(temp_p)
            self.add_system(temp_s)
        # -- load processors --
        for s in json_object["_systemList"]:
            for p in s["_processorList"]:
                temp_processor = Processor(name=p["_name"], description=p["_description"])
                temp_processor.runs_rap_backbone = p["rap_backbone"]
                temp_processor.ip = p["_IP"]
                # processor bindings
                for binding in p["_bindingList"]:
                    # find the system and append
                    for sys in self.systems:
                        if sys.name == s["_name"]:
                            for comp in sys.processes:
                                if binding["_name"] == comp.name:
                                    temp_processor.add_processor_binding(process=comp)
                # processor properties
                for prop in p["_propertyList"]:
                    temp_prop = ""
                    # TODO: extend the AADLIL TO SUPPORT PROCESSOR PROPERTIES

                # processor features
                for f in p["_featureList"]:
                    _m = None
                    for m in self.messages:
                        if f["_message"] is not None:
                            if m.name == f["_message"]["_name"]:
                                _m = m
                    if f["_featureType"] == "inport":
                        temp_f = InPort(name=f["_name"], type=f["_type"], message=_m)
                    elif f["_featureType"] == "outport":
                        temp_f = OutPort(name=f["_name"], type=f["_type"], message=_m)
                    elif f["_featureType"] == "port":
                        temp_f = OutPort(name=f["_name"], type=f["_type"], initial_value=f["_initialValue"], value_reference=f["_valueReference"], message=_m)
                    else:
                        temp_f = ""
                    temp_processor.add_feature(feature=temp_f)
                for _s in self.systems:
                    if _s.name == s["_name"]:
                        _s.add_processor(processor=temp_processor)

    def __eq__(self, other):
        if not isinstance(other, System):
            return NotImplemented
        return self.__dict__ == other.__dict__

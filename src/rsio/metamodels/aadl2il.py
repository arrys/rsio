import json
from pathlib import Path
from typing import Callable


class NamedObject:

    def __init__(self, name: str, description: str, verbose: bool):
        self.name = name
        self.description = description
        self.verbose = verbose


class Process(NamedObject):

    # TODO Change formalism type and expand list types
    def __init__(self, name: str="tbd", description: str="tbd", verbose: bool=False, features: list | None=None, threads: list | None=None, formalism: str="python", containerization: bool=False):
        super().__init__(name=name, description=description, verbose=verbose)
        self.features = features if features else []
        self.threads = threads if threads else []
        self.formalism = formalism
        self.containerization = containerization

    def add_feature(self, feature):
        self.features.append(feature)

    def add_thread(self, t):
        self.threads.append(t)


class Thread(NamedObject):

    def __init__(self, name: str="tbd", description: str="tbd", verbose: bool=False, features: list | None=None, event_trigger=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.features = features if features else []
        self.event_trigger = event_trigger

    def add_feature(self, feature):
        self.features.append(feature)


class Characteristic(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, value:str="", data_type:str="-"):
        super().__init__(name=name, description=description, verbose=verbose)
        self.value = value
        self.data_type = data_type


class Event(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False):
        super().__init__(name=name, description=description, verbose=verbose)


class Mode(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, callback:Callable | None=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.callback = callback


class Transition(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, callback:Callable | None=None, source=None, destination=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.source = source
        self.destination = destination
        self.callback = callback


class Feature(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, feature_type:str="feature"):
        super().__init__(name=name, description=description, verbose=verbose)
        self.feature_type = feature_type


class Port(Feature):

    def __init__(self, name:str="tbd", description:str="tbd", initial_value: float=1.0, value_reference: int=1, port_type:str="data", message=None, verbose=False):
        super().__init__(name=name, description=description, verbose=verbose)
        self.feature_type = "port"
        self.value = initial_value
        self.value_reference = value_reference
        self.port_type = port_type
        self.message = message


class InPort(Port):
    def __init__(self, name:str="tbd", description:str="tbd", initial_value:float=1.0, value_reference:int=1, port_type:str="data", verbose=False, message=None):
        super().__init__(name=name, description=description, verbose=verbose, initial_value=initial_value, value_reference=value_reference, port_type=port_type, message=message)
        self.feature_type = "inport"


class OutPort(Port):
    def __init__(self, name:str="tbd", description:str="tbd", initial_value:float=1.0, value_reference:int=1, port_type:str="data", verbose=False, message=None):
        super().__init__(name=name, description=description, verbose=verbose, initial_value=initial_value, value_reference=value_reference, port_type=port_type, message=message)
        self.feature_type = "outport"


class Connection(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, source=None, destination=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.source = source
        self.destination = destination


class Message(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, features: list | None =None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.features = features if features else []

    def add_feature(self, feature):
        """Add a feature to the system """
        self.features.append(feature)


class Data(Feature):

    def __init__(self, name:str="tbd", description:str="tbd", data_type:str="Float_64", verbose:bool=False):
        super().__init__(name=name, description=description, verbose=verbose)
        self.data_type = data_type


class Processor(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, features=None, properties=None, bindings=None, ip:str="localhost"):
        super().__init__(name=name, description=description, verbose=verbose)
        self.features = features if features else []
        self.properties = properties if properties else []
        self.bindings = bindings if bindings else []
        self.ip = ip
        self.rap_backbone = False

    def add_feature(self, feature):
        self.features.append(feature)

    def add_property(self, p):
        self.properties.append(p)

    def add_processor_binding(self, process):
        """Add a processor binding to the processor."""
        self.bindings.append(process)

    @property
    def processor_binding(self):
        return self.bindings


class Memory(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, properties: list | None=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.properties = properties if properties else []

    def add_property(self, p):
        self.properties.append(p)


class Bus(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, properties: list | None=None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.properties = properties if properties else []
        self.connections = []

    def add_property(self, p):
        self.properties.append(p)

    def add_connection(self, p):
        self.connections.append(p)


class System(NamedObject):

    def __init__(self, name:str="tbd", description:str="tbd", verbose:bool=False, systems=None, processes=None, features=None, messages=None, processors=None, package="", prefix="", json_descriptor: Path | None = None):
        super().__init__(name=name, description=description, verbose=verbose)
        self.features = features if features else []
        self.systems = systems if systems else []
        self.processes = processes if processes else []
        self.messages = messages if messages else []
        self.processors = processors if processors else []
        if json_descriptor: # TODO Change to class method
            self.json2object(json_descriptor=json_descriptor)

    def add_process(self, process):
        self.processes.append(process)

    def add_system(self, system):
        self.systems.append(system)

    def add_feature(self, feature):
        self._feature_list.append(feature)

    def add_message(self, message):
        self.messages.append(message)

    def add_processor(self, processor):
        self.processors.append(processor)

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
        self.name = json_object["name"]
        self.description = json_object["description"]
        # -- load messages --
        for m in json_object["messages"]:
            features = []
            for d in m["features"]:
                temp_d = Data(name=d["name"], data_type=d["data_type"])
                features.append(temp_d)
            temp_message = Message(name=m["name"], features=features)
            self.add_message(temp_message)
        # -- load systems and containing processes --
        for s in json_object["systems"]:
            temp_s = System(name=s["name"], description=s["description"])
            for p in s["processes"]:
                temp_p = Process(name=p["name"], description=p["description"])
                features = []
                for f in p["features"]:
                    _m = None
                    for m in self.messages:
                        if f["message"] is not None:
                            if m.name == f["message"]["name"]:
                                _m = m
                    if f["feature_type"] == "inport":
                        temp_f = InPort(name=f["name"], port_type=f["port_type"], message=_m)
                    elif f["feature_type"] == "outport":
                        temp_f = OutPort(name=f["name"], port_type=f["port_type"], message=_m)
                    else:
                        temp_f = ""
                    temp_p.add_feature(temp_f)
                threads = []
                for t in p["threads"]:
                    tfeatures = []
                    for f in t["features"]:
                        _m = None
                        for m in self.messages:
                            if f["message"] is not None:
                                if m.name == f["message"]["name"]:
                                    _m = m
                        if f["feature_type"] == "inport":
                            temp_f = InPort(name=f["name"], port_type=f["port_type"], message=_m)
                        elif f["feature_type"] == "outport":
                            temp_f = OutPort(name=f["name"], port_type=f["port_type"], message=_m)
                        else:
                            temp_f = ""
                        tfeatures.append(temp_f)
                    temp_t = Thread(name=t["name"], features=tfeatures, event_trigger=t["event_trigger"])
                    temp_p.add_thread(temp_t)
                temp_p.formalism = p["formalism"]
                temp_p.containerization = p["containerization"]
                temp_s.add_process(temp_p)
            self.add_system(temp_s)
        # -- load processors --
        for s in json_object["systems"]:
            for p in s["processors"]:
                temp_processor = Processor(name=p["name"], description=p["description"])
                temp_processor.runs_rap_backbone = p["rap_backbone"]
                temp_processor.ip = p["ip"]
                # processor bindings
                for binding in p["bindings"]:
                    # find the system and append
                    for sys in self.systems:
                        if sys.name == s["name"]:
                            for comp in sys.processes:
                                if binding["name"] == comp.name:
                                    temp_processor.add_processor_binding(process=comp)
                # processor properties
                for prop in p["properties"]:
                    temp_prop = ""
                    # TODO: extend the AADLIL TO SUPPORT PROCESSOR PROPERTIES

                # processor features
                for f in p["features"]:
                    _m = None
                    for m in self.messages:
                        if f["message"] is not None:
                            if m.name == f["message"]["name"]:
                                _m = m
                    if f["feature_type"] == "inport":
                        temp_f = InPort(name=f["name"], port_type=f["port_type"], message=_m)
                    elif f["feature_type"] == "outport":
                        temp_f = OutPort(name=f["name"], port_type=f["port_type"], message=_m)
                    elif f["feature_type"] == "port":
                        temp_f = OutPort(name=f["name"], port_type=f["port_type"], initial_value=f["value"], value_reference=f["value_reference"], message=_m)
                    else:
                        temp_f = ""
                    temp_processor.add_feature(feature=temp_f)
                for _s in self.systems:
                    if _s.name == s["name"]:
                        _s.add_processor(processor=temp_processor)

    def __eq__(self, other):
        if not isinstance(other, System):
            return NotImplemented
        return self.__dict__ == other.__dict__

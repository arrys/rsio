import logging
import re
import sys
from pathlib import Path
from rsio.metamodels.aadl2il import System, Process, InPort, OutPort, Thread, Data, Message
from rsio.utils.exit import ExitCode


class AadlParser:
    """This is a parser that parses multiple AADL files and puts them into the AADL intermediate language."""

    def __init__(self, logical_architecture: Path, physical_architecture: Path, messages: Path):
        self.adaptive_system = None
        self.managing_system = None
        self.managed_system = None
        self.messages = []
        self.processes = []
        self.logger = logging.getLogger(__name__)

        # Read the logical architecture
        try:
            self.logical_architecture_aadl = logical_architecture.read_text()
        except FileNotFoundError:
            self.logical_architecture_aadl = None
            self.logger.fatal(f"Error: File '{logical_architecture}' not found.")
            sys.exit(ExitCode.DATA_ERROR)

        # Read the physical architecture
        try:
            self.physical_architecture_aadl = physical_architecture.read_text()
        except FileNotFoundError:
            self.physical_architecture_aadl = None
            self.logger.fatal(f"Error: File '{physical_architecture}' not found.")
            # sys.exit(ExitCode.DATA_ERROR) #TODO: enable when implemented

        # Read the messages
        try:
            self.messages_aadl = messages.read_text()
        except FileNotFoundError:
            self.messages_aadl = None
            self.logger.fatal(f"Error: File '{messages}' not found.")
            sys.exit(ExitCode.DATA_ERROR)

    def aadl2aadl_il(self) -> System:
        """Function to parse the AADL models and put them into the AADL intermediate language."""

        # 0. Setup adaptive system
        self.adaptive_system = System(name="adaptiveSystem", description="Generated from AADL models")

        # 1. Setup managing and managed system
        self.managed_system = System(name="managedSystem", description="managed system part")
        self.managing_system = System(name="managingSystem", description="managing system part")

        # 1. Parse the messages
        self._generate_messages()
        self.adaptive_system.messages = self.messages

        # 2. Parse the processes
        self._generate_processes()

        # 3. Populate adaptive system
        self.adaptive_system.add_system(self.managing_system)
        self.adaptive_system.add_system(self.managed_system)

        return self.adaptive_system

    def _generate_processes(self):
        """Function to parse the AADL processes."""

        # Find all matches with "process" followed by any word
        pattern = r'process\s+([\w:]+)'
        matches = re.findall(pattern, self.logical_architecture_aadl, re.DOTALL)
        # Filter out matches containing "implementation"
        filtered_matches = [match for match in matches if "implementation" not in match]
        # Generate process components for each of the matches
        for match in filtered_matches:
            p = Process(name=match, description=match + " component")

            # add features to the process
            pattern = r"process " + match + "(.*?)end " + match + ";"
            matches = re.findall(pattern, self.logical_architecture_aadl, re.DOTALL)
            feature_pattern = r'(\w+):\s+(in|out)\s+(event|data|event data)\s+port\s+([\w:]+);'
            matches = re.findall(feature_pattern, matches[0], re.DOTALL)
            for feature in matches:
                # Lambda function to find an object by name
                find_by_name = lambda name: next((item for item in self.messages if item.name == name), None)

                if feature[1] == "in":
                    f = InPort(name=feature[0], port_type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                    p.add_feature(f)
                elif feature[1] == "out":
                    f = OutPort(name=feature[0], port_type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                    p.add_feature(f)

            # add threads to the process
            try:
                pattern = r"process implementation " + match + ".impl(.*?)end " + match + ".impl;"
                matches = re.findall(pattern, self.logical_architecture_aadl, re.DOTALL)
                thread_pattern = r'(\w+): thread\s+([\w:]+);'
                thread_components = re.findall(thread_pattern, matches[0], re.DOTALL)
                feature_list = []
                # fetch thread content
                for t in thread_components:
                    pattern = r"thread " + t[0] + "(.*?)end " + t[0] + ";"
                    matches = re.findall(pattern, self.logical_architecture_aadl, re.DOTALL)
                    matches = re.findall(feature_pattern, matches[0], re.DOTALL)
                    for feature in matches:
                        # Lambda function to find an object by name
                        find_by_name = lambda name: next((item for item in self.messages if item.name == name), None)

                        if feature[1] == "in":
                            f = InPort(name=feature[0], port_type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                            feature_list.append(f)
                        elif feature[1] == "out":
                            f = OutPort(name=feature[0], port_type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                            feature_list.append(f)

                th = Thread(name=t[0], features=feature_list)
                p.add_thread(th)

            except:
                self.logger.warning(f"Process {match} does not have an implementation")

            self.processes.append(p)
            # add to the managing system or managed system
            if "monitor" in p.name or "analysis" in p.name or "plan" in p.name or "legitimate" in p.name or "execute" in p.name:  # TODO: check if this is ok for the user
                self.managing_system.add_process(p)
            elif "knowledge" not in p.name:
                self.managed_system.add_process(p)
        return self.processes

    def _generate_messages(self):
        """Function to parse the AADL messages."""

        # Find all matches with the "data" pattern
        pattern = r"data (\w+)(.*?)end \1;"
        matches = re.findall(pattern, self.messages_aadl, re.DOTALL)
        for match in matches:
            name = match[0]

            # --- SIMPLE MESSAGES, EXTRACT FEATURES
            feature_pattern = r"(\w+): provides data access ([\w:]+);"
            features = re.findall(feature_pattern, match[1])
            feature_list = []
            for feature in features:
                if "::" in feature[1]:
                    f = Data(name=feature[0], data_type=feature[1].split("::")[1])
                else:
                    f = Data(name=feature[0], data_type=feature[1])
                feature_list.append(f)
            m = Message(name=name, features=feature_list)
            self.messages.append(m)
        return self.messages

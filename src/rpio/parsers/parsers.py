import os
import re
import sys
from rpio.metamodels.aadl2_IL import *
from textx import metamodel_from_file


class AADL_parser:
    """This is a parser that parses multiple AADL files and puts them into the AADL intermediate language.

        :param [logicalArchitecture]: [Path to the logical architecture AADL model], defaults to [None]
        :type [logicalArchitecture]: [string](, optional)

        :param [logicalArchitecture]: [Path to the logical architecture AADL model], defaults to [None]
        :type [logicalArchitecture]: [string](, optional)

        :param [messages]: [Path to the messages AADL model], defaults to [None]
        :type [messages]: [string](, optional)

        """

    def __init__(self, logical_architecture, physical_architecture, messages):
        """Constructor method
        """
        self.adaptive_system = None
        self.managing_system = None
        self.managed_system = None

        self.messages = []
        self.processes = []

        # Read the logical architecture
        try:
            with open(logical_architecture, 'r') as file:
                self.logical_architecture_aadl = file.read()
        except FileNotFoundError:
            self.logical_architecture_aadl = None
            print(f"Error: File '{logical_architecture}' not found.")
            sys.exit(1)

        # Read the physical architecture
        try:
            with open(physical_architecture, 'r') as file:
                self.physical_architecture_aadl = file.read()
        except FileNotFoundError:
            self.physical_architecture_aadl = None
            print(f"Error: File '{physical_architecture}' not found.")
            # sys.exit(1)        #TODO: enable if implemented

        # Read the messages
        try:
            with open(messages, 'r') as file:
                self.messages_aadl = file.read()
        except FileNotFoundError:
            self.messages_aadl = None
            print(f"Error: File '{messages}' not found.")
            sys.exit(1)

    def aadl2aadl_il(self):
        """Function to parse the AADL models and put them into the AADL intermediate language

        :return: [adaptiveSystem]
        :rtype: [Object]
        """

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
                    f = InPort(name=feature[0], type=feature[2], message=find_by_name(feature[3].split("::")[1]))
                    p.add_feature(f)
                elif feature[1] == "out":
                    f = OutPort(name=feature[0], type=feature[2], message=find_by_name(feature[3].split("::")[1]))
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
                            f = InPort(name=feature[0], type=feature[2],
                                       message=find_by_name(feature[3].split("::")[1]))
                            feature_list.append(f)
                        elif feature[1] == "out":
                            f = OutPort(name=feature[0], type=feature[2],
                                        message=find_by_name(feature[3].split("::")[1]))
                            feature_list.append(f)

                th = Thread(name=t[0], feature_list=feature_list)
                p.add_thread(th)

            except:
                print(f"Process {match} does not have an implementation")

            self.processes.append(p)
            # add to the managing system or managed system
            if 'monitor' in p.name or 'analysis' in p.name or 'plan' in p.name or 'legitimate' in p.name or 'execute' in p.name:  # TODO: check if this is ok for the user
                self.managing_system.add_process(p)
            elif 'knowledge' not in p.name:
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
                if '::' in feature[1]:
                    f = Data(name=feature[0], data_type=feature[1].split("::")[1])
                else:
                    f = Data(name=feature[0], data_type=feature[1])
                feature_list.append(f)
            m = Message(name=name, feature_list=feature_list)
            self.messages.append(m)
        return self.messages


class RobochartParser:
    """This is a parser that parses multiple robochart files, as input for the AADL code generator.

        :param [MAPLEK]: [Path to the MAPLE-K roboChart model], defaults to [None]
        :type [MAPLEK]: [string](, optional)

        :param [Monitor]: [Path to the Monitor roboChart model], defaults to [None]
        :type [Monitor]: [string](, optional)

        :param [Analysis]: [Path to the Analysis roboChart model], defaults to [None]
        :type [Analysis]: [string](, optional)

        :param [Plan]: [Path to the Plan roboChart model], defaults to [None]
        :type [Plan]: [string](, optional)

        :param [Legitimate]: [Path to the Legitimate roboChart model], defaults to [None]
        :type [Legitimate]: [string](, optional)

        :param [Execute]: [Path to the Execute roboChart model], defaults to [None]
        :type [Execute]: [string](, optional)

        :param [Knowledge]: [Path to the Knowledge roboChart model], defaults to [None]
        :type [Knowledge]: [string](, optional)

        """

    def __init__(self, maplek, monitor, analysis, plan, legitimate, execute, knowledge):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        metamodel_path = os.path.join(current_dir, 'robochart/robochart.tx')
        self.robochart_meta = metamodel_from_file(metamodel_path)

        self.maplek_model = None
        self.monitor_model = None
        self.analysis_model = None
        self.plan_model = None
        self.legitimate_model = None
        self.execute_model = None
        self.knowledge_model = None

        # Read the MAPLE-K robochart model
        try:
            self.maplek_model = self.robochart_meta.model_from_file(maplek)
        except FileNotFoundError:
            self.maplek_model = None
            print(f"Error: File '{maplek}' not found.")
            sys.exit(1)

        # Read the Monitor robochart model
        try:
            self.monitor_model = self.robochart_meta.model_from_file(monitor)
        except FileNotFoundError:
            self.monitor_model = None
            print(f"Error: File '{monitor}' not found.")
            sys.exit(1)

        # Read the Analysis robochart model
        try:
            self.analysis_model = self.robochart_meta.model_from_file(analysis)
        except FileNotFoundError:
            self.analysis_model = None
            print(f"Error: File '{analysis}' not found.")
            sys.exit(1)

        # Read the Plan robochart model
        try:
            self.plan_model = self.robochart_meta.model_from_file(plan)
        except FileNotFoundError:
            self.plan_model = None
            print(f"Error: File '{plan}' not found.")
            sys.exit(1)

        # Read the Legitimate robochart model
        try:
            self.legitimate_model = self.robochart_meta.model_from_file(legitimate)
        except FileNotFoundError:
            self.legitimate_model = None
            print(f"Error: File '{legitimate}' not found.")
            sys.exit(1)

        # Read the Execute robochart model
        try:
            self.execute_model = self.robochart_meta.model_from_file(execute)
        except FileNotFoundError:
            self.execute_model = None
            print(f"Error: File '{execute}' not found.")
            sys.exit(1)

        # Read the Knowledge robochart model
        try:
            self.knowledge_model = self.robochart_meta.model_from_file(knowledge)
        except FileNotFoundError:
            self.knowledge_model = None
            print(f"Error: File '{knowledge}' not found.")
            sys.exit(1)

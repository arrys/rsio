import os
from pathlib import Path


class PackageManager(object):

    def __init__(self, name='PackageManager', description='Built-in package manager', verbose=False):
        """"""
        self._name = name
        self._description = description
        self._verbose = verbose

        self._package_name = "rpio_pkg"
        self.standalone_path = ""
        self._directory = os.getcwd()

    @property
    def name(self):
        """The name property (read-only)."""
        return self._name

    @property
    def description(self):
        """The description property (read-only)."""
        return self._description

    def create(self, name, force=False, standalone=False, path=None):
        """"""
        is_empty = self._check_empty_dir()

        if not standalone:
            if is_empty or (not is_empty and force):
                if self._verbose: print("DEBUG: directory is empty, creating " + self._package_name + " package...")
                # --- rpio package creation ---
                try:
                    self._populate_package(name=name, standalone=standalone)
                except:
                    raise Exception("ERROR: " + self._package_name + " package could not be created!")

                if self._verbose: print("DEBUG: " + self._package_name + " package created...")
            else:
                if self._verbose: print("DEBUG: directory is not empty, no " + self._package_name + " package created!")
        else:
            if path is not None:
                self.standalone_path = path
                try:
                    self._populate_package(name=name, standalone=standalone)
                    if self._verbose: print("DEBUG: " + self._package_name + " package created...")
                except:
                    raise Exception("ERROR: " + self._package_name + " package could not be created!")

            else:
                self.standalone_path = os.getcwd()
                try:
                    self._populate_package(name=name, standalone=standalone)
                    if self._verbose: print("DEBUG: " + self._package_name + " package created...")
                except:
                    raise Exception("ERROR: " + self._package_name + " package could not be created!")

    def check(self, path: str | Path = None) -> bool:
        """"""
        path = path if path else Path.cwd()
        package_path = path if isinstance(path, Path) else Path(path)
        if self._verbose: print(f"DEBUG: checking {self._package_name} package in {package_path}...")
        is_valid_package = (package_path / "robosapiensIO.ini").is_file()
        # TODO: add other checks
        return is_valid_package

    def _check_empty_dir(self):
        """Function to determine if a directory is empty."""
        if self._verbose: print("DEBUG: Checking if directory is empty...")
        return len(os.listdir(self._directory)) == 0

    def _populate_package(self, name="rpio_pkg", standalone=False):
        """Function to populate the empty package."""
        self._package_name = name
        if standalone:
            # generate in standalone package instead of in current directory
            Path(self.standalone_path + "/" + self._package_name).mkdir(parents=True, exist_ok=True)
            prefix = self.standalone_path + "/" + self._package_name + '/'
            self._add_file(file="robosapiensIO.ini", name=self._package_name, path=prefix)
            self._add_file(file="__init__.py", name=self._package_name, path=prefix)
            logfilepath = prefix + "/Resources"
        else:
            prefix = ""
            self._add_file(file="robosapiensIO.ini", name=self._package_name)
            self._add_file(file="__init__.py", name=self._package_name)
            logfilepath = self._directory + "/Resources"

        self._mkdir_custom(prefix + "Documentation")
        self._mkdir_custom(prefix + "Concept")
        self._mkdir_custom(prefix + "Design")
        self._mkdir_custom(prefix + "Realization")
        # managing system
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Documentation")
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Binaries")
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Nodes")
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Messages")
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Platform")
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Actions")
        self._mkdir_custom(prefix + "Realization/ManagingSystem/Workflows")
        # managed system
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Documentation")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Binaries")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Nodes/Probes")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Nodes/Effector")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Messages")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Platform")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Actions")
        self._mkdir_custom(prefix + "Realization/ManagedSystem/Workflows")
        # top-level workflows
        self._mkdir_custom(prefix + "Workflows")
        self._add_file(file="AADL2CODE.py", path=prefix + "Workflows/")
        self._add_file(file="ROBOCHART2AADL.py", path=prefix + "Workflows/")
        # temporary folder and resources
        self._mkdir_custom(prefix + "Resources")

        # add system log file
        self._add_file(file="sys.log", path=logfilepath)

        # add run, build and deploy actions (placeholders) for managing system
        self._add_file(file="run.py", path=prefix + "Realization/ManagingSystem/Actions/")
        self._add_file(file="build.py", path=prefix + "Realization/ManagingSystem/Actions/")
        self._add_file(file="deploy.py", path=prefix + "Realization/ManagingSystem/Actions/")

        # add run, build and deploy actions (placeholders) for managed system
        self._add_file(file="run.py", path=prefix + "Realization/ManagedSystem/Actions/")
        self._add_file(file="build.py", path=prefix + "Realization/ManagedSystem/Actions/")
        self._add_file(file="deploy.py", path=prefix + "Realization/ManagedSystem/Actions/")

    def _mkdir_custom(self, folder="empty", file='readme.md'):
        """mkdir function to initialize git-pushable directories"""
        Path(folder).mkdir(parents=True, exist_ok=True)
        self._add_file(file=file, path=folder)

    def _add_file(self, file="requirements.txt", name="", description="", path=None):
        """Function to add a file to the provided path."""

        if path == None:
            path = self._directory
        f = open(path + "/" + file, "a")

        if "__init__.py" in file:
            f.write("")

        if "readme" in file:
            f.write("Placeholder")

        if "sys.log" in file:
            f.write("---------------------- RoboSAPIENS Adaptive Platform system logs ----------------------\n")

        if "robosapiensIO.ini" in file:
            f.write("[RoboSAPIENSIO]\n")
            f.write('name = ' + name + '\n')
            f.write('description = " Add project description"\n')
            f.write('\n')
            f.write("[PACKAGE]\n")
            f.write("name = " + name + "\n")
            f.write('prefix =  \n')

        if "run.py" in file:
            f.write("print('WARNING: Run action not implemented yet!')")

        if "build.py" in file:
            f.write("print('WARNING: Build action not implemented yet!')")

        if "deploy.py" in file:
            f.write("print('WARNING: Deploy action not implemented yet!')")

        if "AADL2CODE.py" in file:
            f.write("# **********************************************************************************\n")
            f.write("# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>\n")
            f.write("# *\n")
            f.write("# * This file is part of the roboarch R&D project.\n")
            f.write("# *\n")
            f.write("# * RAP R&D concepts can not be copied and/or distributed without the express\n")
            f.write("# * permission of Bert Van Acker\n")
            f.write("# **********************************************************************************\n")
            f.write("from rpio.workflow.tasks import *\n")
            f.write("from rpio.workflow.executer import Executer_GUI\n")
            f.write("\n")
            f.write("# 1 . define the tasks\n")
            f.write("tasks = {\n")
            f.write('    "Generate custom messages": t_generate_messages,\n')
            f.write('    "Generate swc code skeletons": t_generate_swc_skeletons,\n')
            f.write('    "Generate swc launch files": t_generate_swc_launch,\n')
            f.write('    "Generate main file": t_generate_main,\n')
            f.write('    "Generate docker compose files": t_generate_docker,\n')
            f.write('    "Update robosapiensIO.ini file": t_update_robosapiensIO_ini\n')
            f.write("}\n")
            f.write("\n")
            f.write("# 2. Launch the graphical executer\n")
            f.write('app = Executer_GUI(tasks=tasks,name="AADL2CODE")\n')
            f.write("app.root.mainloop()\n")

        if "ROBOCHART2AADL.py" in file:
            f.write("# **********************************************************************************\n")
            f.write("# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>\n")
            f.write("# *\n")
            f.write("# * This file is part of the roboarch R&D project.\n")
            f.write("# *\n")
            f.write("# * RAP R&D concepts can not be copied and/or distributed without the express\n")
            f.write("# * permission of Bert Van Acker\n")
            f.write("# **********************************************************************************\n")
            f.write("from rpio.workflow.tasks import *\n")
            f.write("from rpio.workflow.executer import Executer_GUI\n")
            f.write("\n")
            f.write("\n")
            f.write("# 1 . define the tasks\n")
            f.write("tasks = {\n")
            f.write('    "Generate AADL messages": t_robochart_to_messages,\n')
            f.write('    "Generate AADL Logical Architecture": t_robochart_to_logical\n')
            f.write("}\n")
            f.write("\n")
            f.write("# 2. Launch the graphical executer\n")
            f.write('app = Executer_GUI(tasks=tasks,name="ROBOCHART2AADL")\n')
            f.write("app.root.mainloop()\n")
        f.close()

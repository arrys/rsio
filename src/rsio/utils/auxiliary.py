import logging
import re
import socket
import sys
import threading
import os
import io
import zipfile
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path

import paho.mqtt.client as mqtt
import redis
import importlib
from subprocess import Popen

from rsio.utils.constants import Formalism, detect_operating_system, OperatingSystem

# Only windoze supports CREATE_NEW_CONSOLE
try:
    from subprocess import CREATE_NEW_CONSOLE
except ImportError:
    pass


def get_custom_code(text: str, tag: str) -> list | None:
    pattern = r"#<!-- cc_" + tag + " START--!>(.*?)#<!-- cc_" + tag + " END--!>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches if matches else None


def replace_custom_code(text: str, tag: str, replacement: str) -> str:
    pattern = r"#<!-- cc_" + tag + " START--!>(.*?)#<!-- cc_" + tag + " END--!>"
    start_tag = "#<!-- cc_" + tag + " START--!>"
    end_tag = "#<!-- cc_" + tag + " END--!>"
    return re.sub(pattern, start_tag + replacement[0] + end_tag, text, flags=re.DOTALL)


def run_command(command: str):
    try:
        # result = subprocess.run(command[0][0], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = Popen(command[0], shell=True, cwd=command[1])
        stdout, stderr = process.communicate()
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run command. Error: {e}")  # decode("utf-8") possible source of exe being flagged as virus
        # print(f"Command: {command}\nError: {e.stderr.decode("utf-8")}")


def execute_commands(commands: list[str]):
    """
    Execute multiple command line functions concurrently.

    Parameters:
    commands (list of str): List of command line commands to execute.
    """
    threads = []
    for command in commands:
        thread = threading.Thread(target=run_command, args=(command,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def extract_commands(launch_description):
    commands = []
    for component in launch_description.components:
        commands.append([component.cmd, component.path])
    return commands


class Component:
    def __init__(self, name: str, path: Path, formalism: Formalism):
        self.name = name
        self.path = path
        if formalism == Formalism.PYTHON:
            self.cmd = ["python", f"{name}.py"]
        if formalism == Formalism.CPP:
            self.cmd = [str(path / f"{name}.exe")]

    def __repr__(self):
        return f"Swc(name='{self.name}', cmd='{self.cmd}')"


class Launch:
    def __init__(self, nodes: list[Component]):
        self.components = nodes

    def __repr__(self):
        return f"Launch(components={self.components})"


def parse_launch_xml(file_path: Path, formalism: Formalism=Formalism.PYTHON):
    root = ET.fromstring(file_path.read_text())
    components = []
    for node_elem in root.findall("node"):
        name = node_elem.get("name")
        path = node_elem.get("path")
        components.append(Component(name, path, formalism))
    return Launch(components)


def decompress_folder(data, output_path):
    # Decompress the byte stream into the output folder
    with zipfile.ZipFile(io.BytesIO(data), "r") as zip_file:
        zip_file.extractall(output_path)
    print(f"Folder decompressed to '{output_path}'.")


def compress_folder(folder_path):
    # Compress the folder into a byte stream
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))
    zip_buffer.seek(0)
    return zip_buffer.read()


def get_pip_path(venv_name: str) -> Path:
    """Returns the path to the pip executable based on the operating system."""
    return Path(venv_name) / "Scripts" / "pip.exe" if os.name == "nt" else Path(venv_name) / "bin" / "pip"

def create_virtual_environment(venv_name="venv"):
    """
    Creates a Python virtual environment.

    :param venv_name: The name of the virtual environment directory. Defaults to "venv".
    """
    if os.path.exists(venv_name):
        print(f"Virtual environment '{venv_name}' already exists. Skipping creation.")
        return

    try:
        # Check if Python is installed
        python_version_check = subprocess.run(["python", "--version"], capture_output=True, text=True)

        # Install virtualenv package if not installed
        subprocess.run(["python", "-m", "pip", "install", "virtualenv"], check=True)

        # Create virtual environment using virtualenv
        subprocess.run(["python", "-m", "virtualenv", venv_name, "--python=python3.10"], check=True)
        print(f"Virtual environment '{venv_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating virtual environment: {e}")


def activate_virtual_environment(venv_name="venv"):
    """
    Activates the virtual environment.
    :param venv_name: The name of the virtual environment directory. Defaults to "venv".
    """
    operating_system = detect_operating_system()
    if operating_system == OperatingSystem.WINDOWS:
        subprocess.run(str(Path(venv_name) / "Scripts" / "activate.bat"), shell=True)
    elif operating_system == OperatingSystem.UNIX:
        subprocess.run(["source", str(Path(venv_name) / "bin" / "activate")], shell=True, executable="/bin/bash")
    else:
        raise RuntimeError("Unsupported operating system.")

# TODO Do we need this?
def deactivate_virtual_environment():
    """Deactivates the virtual environment."""
    operating_system = detect_operating_system()
    if operating_system == OperatingSystem.WINDOWS:
        subprocess.run("deactivate", shell=True)
    elif operating_system == OperatingSystem.UNIX:
        subprocess.run("deactivate", shell=True, executable="/bin/bash")
    else:
        raise RuntimeError("Unsupported operating system.")

def install_python_packages_from_requirements_file(requirements_file: Path, venv_name: str | None = "venv") -> bool:
    """
    Installs packages listed in a requirements.txt file into the virtual or native environment.

    :param venv_name: The name of the virtual environment directory. Defaults to "venv".
    :param requirements_file: The path to the requirements.txt file. Defaults to "requirements.txt".
    """
    if not requirements_file.is_file():
        raise FileNotFoundError(f"File '{requirements_file}' does not exist.")

    logger = logging.getLogger(__name__)
    if isinstance(venv_name, str):
        pip_path = get_pip_path(venv_name)
        if not pip_path.exists():
            logger.warning(f"Pip not found in the virtual environment '{venv_name}'. Make sure the virtual environment is created.")
            return False
    else:
        pip_path = "pip"
        logger.info("Using pip of native python environment.")

    try:
        subprocess.run([pip_path, "install", "-r", str(requirements_file)], check=True, capture_output=True, text=True)
        logger.info(f"Packages from '{requirements_file}' installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while installing requirements: {e}")
        return False


def get_python_version() -> str:
    """
    Check and return the current Python version installed on the system.
    :return: string representing the Python version.
    :rtype: str or None
    """
    version_info = sys.version_info
    return f"{version_info.major}.{version_info.minor}.{version_info.micro}"


def build_docker_image(docker_file_path: Path, image_name: str) -> bool:
    """
    Build a Docker image for a Python module at a given path.

    :param docker_file_path: Path Dockerfile
    :param image_name: Name of the Docker image to be created
    """
    if not docker_file_path.is_file():
        raise FileNotFoundError(f"No Dockerfile found in the specified module path '{docker_file_path}'.")
    command = ["docker", "build", "-t", image_name, str(docker_file_path)]
    logger = logging.getLogger(__name__)
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Successfully built Docker image '{image_name}' from '{docker_file_path}'.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to build Docker image. Error: {e}")
        return False

def run_docker_container(image_name: str, container_name: str | None = None, ports: dict[int, int] | None=None) -> bool:
    """
    Run a Docker container from an existing image.

    :param image_name: Name of the Docker image to run
    :param container_name: Optional name for the container
    :param ports: Optional dictionary mapping container ports to host ports (e.g., {"8080": "8080"})
    :return: None
    """
    command = ["docker", "run", "-d"]
    if container_name:
        command.extend(["--name", container_name])
    if ports:
        for host_port, container_port in ports.items():
            command.extend(["-p", f"{host_port}:{container_port}"])
    command.append(image_name)
    logger = logging.getLogger(__name__)
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Successfully started container from image '{image_name}'.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run Docker container. Error: {e}")
        return False

def get_docker_version() -> str | bool:
    """
    Check if Docker is installed on the system
    :return: String with the docker version if Docker is installed, False otherwise
    """
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

@dataclass
class RedisConfiguration:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    socket_timeout: int = 5

def is_redis_reachable(redis_configuration: RedisConfiguration=RedisConfiguration()) -> bool:
    """
    Check if Redis is running and reachable
    :return: True if Redis is running and reachable, False otherwise
    """
    try:
        client = redis.Redis(**asdict(redis_configuration))
        if client.ping():
            return True  # Redis is reachable
    except redis.exceptions.ConnectionError:
        pass
    return False

@dataclass
class MqttConfiguration:
    host: str = "localhost"
    port: int = 1883
    keepalive: int = 5

def is_mqtt_reachable(mqtt_configuration: MqttConfiguration=MqttConfiguration()) -> bool:
    """
    Check if MQTT is running and reachable
    :return: True if MQTT broker is running and reachable, False otherwise
    """
    client = mqtt.Client(protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    try:
        client.connect(**asdict(mqtt_configuration))
        client.disconnect()
        return True
    except (ConnectionRefusedError, TimeoutError, OSError, socket.error):
        return False


def is_python_package_installed(package: str) -> bool:
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False

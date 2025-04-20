import re
import threading
import os
import io
import zipfile
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import paho.mqtt.client as mqtt
import yaml
import redis
import importlib
from subprocess import Popen

from rsio.utils.constants import Formalism

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


def get_activate_script_path(venv_name):
    """Returns the path to the activated script based on the operating system."""
    return os.path.join(venv_name, "Scripts", "activate.bat") if os.name == "nt" else os.path.join(venv_name, "bin", "activate")


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
    activate_script = get_activate_script_path(venv_name)
    if not os.path.exists(activate_script):
        print(
            f"Activate script not found in the virtual environment '{venv_name}'. Make sure the virtual environment is created.")
        return

    if os.name == "nt":
        subprocess.run(activate_script, shell=True)
    else:
        subprocess.run(["source", activate_script], shell=True, executable="/bin/bash")


def deactivate_virtual_environment():
    """
    Deactivates the virtual environment.
    """
    if os.name == "nt":
        subprocess.run("deactivate", shell=True)
    else:
        subprocess.run("deactivate", shell=True, executable="/bin/bash")


def install_requirements(venv_name: str | None = "venv", requirements_file: Path = Path("requirements.txt")):
    """
    Installs packages listed in a requirements file into the virtual or native environment.

    :param venv_name: The name of the virtual environment directory. Defaults to "venv".
    :param requirements_file: The path to the requirements.txt file. Defaults to "requirements.txt".
    """
    if venv_name is not None:
        pip_path = get_pip_path(venv_name)
        if not pip_path.exists():
            print(f"Pip not found in the virtual environment '{venv_name}'. Make sure the virtual environment is created.")
            return
    else:
        pip_path = "pip"
        print("Using pip of native python environment.")

    if not requirements_file.is_file():
        print(f"Requirements file '{requirements_file}' not found.")
        return

    try:
        subprocess.run([pip_path, "install", "-r", str(requirements_file)], check=True)
        print(f"Packages from '{requirements_file}' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing requirements: {e}")


def get_python_version() -> str | None:
    """
    Checks and returns the current Python version installed on the system.

    :return: A string representing the Python version, or None if an error occurs.
    :rtype: str or None
    """
    try:
        # Run the command to get the Python version
        result = subprocess.run(["python", "--version"], capture_output=True, text=True, check=True)
        # Output is usually in the form of "Python X.Y.Z\n"
        version = result.stdout.strip()
        return version
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while checking Python version: {e}")
        return None


def build_docker_image(module_path: str, image_name: str):
    """
    Build a Docker image for a Python module at a given path.

    :param module_path: Path to the module (should contain Dockerfile)
    :param image_name: Name of the Docker image to be created
    :return: None
    """
    if not os.path.isdir(module_path):
        raise FileNotFoundError(f"The specified module path '{module_path}' does not exist or is not a directory.")

    dockerfile_path = os.path.join(module_path, "Dockerfile")
    if not os.path.isfile(dockerfile_path):
        raise FileNotFoundError(f"No Dockerfile found in the specified module path '{module_path}'.")

    try:
        # Build the Docker image using the specified Dockerfile
        command = ["docker", "build", "-t", image_name, module_path]
        subprocess.run(command, check=True)
        print(f"Successfully built Docker image '{image_name}' from '{module_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to build Docker image. Error: {e}")


def run_docker_container(image_name, container_name=None, ports=None):
    """
    Run a Docker container from an existing image.

    :param image_name: Name of the Docker image to run
    :param container_name: Optional name for the container
    :param ports: Optional dictionary mapping container ports to host ports (e.g., {"8080": "8080"})
    :return: None
    """
    try:
        # Prepare the docker run command
        command = ["docker", "run", "-d"]

        if container_name:
            command.extend(["--name", container_name])

        if ports:
            for host_port, container_port in ports.items():
                command.extend(["-p", f"{host_port}:{container_port}"])

        command.append(image_name)

        # Run the Docker container
        subprocess.run(command, check=True)
        print(f"Successfully started container from image '{image_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run Docker container. Error: {e}")


def get_docker_version():
    """
    Check if Docker is installed on the system

    :return: String with docker version if Docker is installed, False otherwise
    """
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        return version
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_redis(host="localhost", port=6379, db=0, timeout=30, config=None):
    """
    Check if Redis is running and reachable

    :return: True if Redis is running and reachable, False otherwise
        """

    try:
        if config is None:
            print("WARNING: configuration file not provided, checking Redis with default values (broker='localhost', port=6379, db=0)")
        else:
            with open(config, "r") as file:
                configuration = yaml.safe_load(file)
                host = configuration["redis_host"]
                port = configuration["redis_port"]

        # Establish a connection with the specified timeout
        client = redis.Redis(host=host, port=port, db=db, socket_timeout=timeout)

        # Ping the server to test connectivity
        if client.ping():
            return True  # Redis is reachable
    except redis.exceptions.ConnectionError:
        pass  # Connection failed

    return False  # Redis is not reachable


def check_mqtt(broker="localhost", port=1883, timeout=30, config=None):
    """
    Check if MQTT is running and reachable

    :return: True if MQTT broker is running and reachable, False otherwise
        """

    def on_connect(client, userdata, flags, rc):
        # If rc (return code) is 0, connection was successful
        client.reachable = (rc == 0)
        client.disconnect()

    client = mqtt.Client()
    client.reachable = False  # Initial assumption: not reachable
    client.on_connect = on_connect

    # resolve the config file for checking the MQTT config
    if config is None:
        print("WARNING: configuration file not provided, checking MQTT with default values (broker='localhost', port=1833)")
    else:
        with open(config, "r") as file:
            configuration = yaml.safe_load(file)
            broker = configuration["mqtt_broker"]
            port = configuration["mqtt_port"]

    # Attempt to connect with a specified timeout
    try:
        client.connect(broker, port, timeout)
        client.loop_start()  # Start the loop to process callbacks
        client.loop(timeout)  # Wait for connection
        client.loop_stop()  # Stop the loop
    except Exception as e:
        print(f"Could not connect to MQTT broker: {e}")

    return client.reachable


def check_package_installation(package="robosapiensio"):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False

from rpio.utils.auxiliary import *
from subprocess import call


def launch(launch_file="launch.xml"):
    """
    Launch one or more Python software components using a launch description file.

    :param launch_file: Launch description file (XML), defaults to "launch.xml"
    :type launch_file: str
    :return: None
    :rtype: None
    """

    # 0. interpret launch file
    launch_description = parse_launch_xml(file=launch_file, formalism="python")

    # 1. launch all commands at once
    execute_commands(extract_commands(launch_description))

def launch_main(main_file="main.py"):
    """
    Launch one or more Python software components using a main file.

    :param main_file: Launch description file (XML), defaults to "launch.xml"
    :type main_file: str
    :return: None
    :rtype: None
    """
    command = ["python", main_file]
    call(command)

def launch_docker_compose(path="/"):
    """
    Launch one or more Python software components using a Docker Compose file.

    :param path: Path to the Docker Compose file for the given platform, defaults to "/"
    :type path: str
    :return: None
    :rtype: None
    """
    try:
        subprocess.Popen(f"docker compose up --build".split(), cwd=path,stdout=subprocess.PIPE)
        return True
    except:
        return False

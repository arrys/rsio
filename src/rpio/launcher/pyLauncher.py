from rpio.utils.auxiliary import *
from subprocess import call


def launch(launchFile='launch.xml'):
    """
    Launch one or more Python software components using a launch description file.

    :param launchFile: Launch description file (XML), defaults to 'launch.xml'
    :type launchFile: str
    :return: None
    :rtype: None
    """

    # 0. interpret launch file
    launchDescription = parse_launch_xml(file=launchFile,formalism="python")

    # 1. launch all commands at once
    execute_commands(extractCommands(launchDescription))

def launch_main(mainFile='main.py'):
    """
    Launch one or more Python software components using a main file.

    :param mainFile: Launch description file (XML), defaults to 'launch.xml'
    :type mainFile: str
    :return: None
    :rtype: None
    """
    command = ["python", mainFile]
    call(command)

def launch_docker_compose(path='/'):
    """
    Launch one or more Python software components using a Docker Compose file.

    :param path: Path to the Docker Compose file for the given platform, defaults to "/"
    :type path: str
    :return: None
    :rtype: None
    """
    try:
        process = subprocess.Popen(f"docker compose up --build".split(), cwd=path,stdout=subprocess.PIPE)
        return True
    except:
        return False

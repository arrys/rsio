import subprocess
from pathlib import Path
from subprocess import call

from rsio.utils.auxiliary import parse_launch_xml, execute_commands, extract_commands
from rsio.utils.constants import Formalism


def launch(launch_file: Path = Path("launch.xml")):
    """Launch one or more Python software components using a launch description file."""
    launch_description = parse_launch_xml(file_path=launch_file, formalism=Formalism.PYTHON)
    execute_commands(extract_commands(launch_description))

def launch_main(main_file: Path = Path("main.py")):
    """Launch one or more Python software components using a main file."""
    command = ["python", str(main_file)]
    call(command)

def launch_docker_compose(path: Path = Path("/")) -> bool:
    """Launch one or more Python software components using a Docker Compose file."""
    try:
        subprocess.Popen(
            ["docker", "compose", "up", "--build"],
            cwd=str(path),
            stdout=subprocess.PIPE
        )
        return True
    except Exception:
        return False

import logging
import sys
from pathlib import Path

import click
import os
import subprocess
from rpio.launcher.launcher import launch, launch_main, launch_docker_compose
from rpio.utils.exit import ExitCode


@click.group()
@click.pass_context
def run_cmds():
    pass


@run_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--platform", "-p", default="none", help="Specify on which platform you want to run the adaptive application, based on the AADL deployment.")
@click.option("--launchfile", is_flag=True, default=False, help="Specify the use of the launchfile to run the adaptive application.")
@click.option("--docker", is_flag=True, default=False, help="Specify the use of docker to run the adaptive application.")
def run(verbose, platform, launchfile, docker):
    """Run the standalone RoboSAPIENS Adaptive Platform application package."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug("Run command under construction...")

    if platform is None:
        logger.debug("Executing the run.py action (Realization/ManagingSystem/Actions/run.py)")
        _directory = os.getcwd()
        run_file = "Realization/ManagingSystem/Actions/run.py"
        arguments = ""
        logger.debug(run_file)

        try:
            subprocess.run(["py.exe", run_file, arguments])
        except:
            logger.fatal("FAIL - Running standalone robosapiensIO application failed")
            sys.exit(ExitCode.FAILURE)
    else:
        if docker:
            logger.debug(f"Executing the adaptive application using the provided docker compose file for platform {platform}")
            try:
                launch_docker_compose(Path("Realization/ManagingSystem/Platform") / platform)
            except:
                logger.fatal("FAIL - Launching the standalone robosapiensIO application failed")
                sys.exit(ExitCode.FAILURE)
        elif launchfile:
            logger.debug(f"Executing the adaptive application using the provided launch file for platform {platform}")
            try:
                launch(Path("Realization/ManagingSystem/Platform") / platform / "launch.xml")
            except:
                logger.fatal("FAIL - Launching the standalone robosapiensIO application failed")
                sys.exit(ExitCode.FAILURE)
        else:
            logger.debug(f"Executing the adaptive application using the provided main file for platform {platform}")
            try:
                launch_main(Path(f"Resources/main_{platform}.py"))
            except:
                logger.fatal("FAIL - Launching the standalone robosapiensIO application failed")
                sys.exit(ExitCode.FAILURE)

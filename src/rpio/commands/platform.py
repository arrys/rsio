import logging
import sys
from pathlib import Path

import click
import yaml

from rpio.utils.auxiliary import check_redis, check_mqtt, create_virtual_environment, parse_launch_xml, \
    install_requirements, activate_virtual_environment
from rpio.utils.constants import formalism_from_name, Formalism, deployment_from_name, Deployment
from rpio.utils.exit import ExitCode


@click.group()
@click.pass_context
def platform_cmds():
    pass


@platform_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--check", is_flag=True, default=False, help="Checking the prerequisites for running the adaptive application on this platform.")
@click.option("--set", "set_flag", is_flag=True, default=False, help="Setting up the prerequisites for running the adaptive application on this platform.")
@click.option("--name", "-n", default="none", help="Specify the platform name, specified within the AADL.")
@click.option("--force", "-f", default="none", help="Force the setup of this platform [native, virtualenv, containerized].")
def platform(verbose: bool, check: bool, set_flag: bool, name: str, force: str):
    """Checking the prerequisites for running the adaptive application on this platform."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)

    if check:
        logging.debug("WARNING: platform check is not implemented yet.")

        if check_redis():
            logging.info("INFO: REDIS connection check is successful.")
        else:
            logging.fatal("ERROR: REDIS connection failed. Please check if the platform is connected to the host running the Redis.")
            sys.exit(ExitCode.FAILURE)

        if check_mqtt():
            logging.info("INFO: MQTT connection check is successful.")
        else:
            logging.fatal("ERROR: MQTT connection failed. Please check if the platform is connected to the host running the MQTT broker.")
            sys.exit(ExitCode.FAILURE)

    if set_flag:
        # NORMAL FLOW, USE AADL INFO FOR SETTING UP THE ENVIRONMENT
        if name != "none":

            # fetch configuration of the platform
            platform_config = Path("Realization/ManagingSystem/Platform") / name / "config.yaml"
            configuration = yaml.safe_load(platform_config.read_text())
            formalism = formalism_from_name(configuration["formalism"])
            environment_type = configuration["environment"]
            containerization = configuration["containerization"]

            # PYTHON-BASED DEPLOYMENT - PYTHON SETUP
            if formalism == Formalism.PYTHON:
                if type == "virtualenv": # TODO Where is this type coming from?
                    try:
                        create_virtual_environment(venv_name="rpiovenv")
                        launch_description = parse_launch_xml(Path("Realization/ManagingSystem/Platform") / name / "launch.xml")
                        for component in launch_description.components:
                            install_requirements(venv_name="rpiovenv", requirements_file=component.path / "requirements.txt")
                        activate_virtual_environment(venv_name="rpiovenv")
                    except:
                        logging.error("ERROR: Could not setup virtual environment for running the adaptive application on this platform.")
                        # TODO Should we exit?
            elif formalism == Formalism.CPP:
                logging.warning("WARNING: C++ platform setup is not implemented yet.")

        if force == "none":
            sys.exit(ExitCode.SUCCESS)
        match deployment_from_name(force):
            case Deployment.VIRTUAL:
                logging.info("INFO: Forcing to setup a virtual python environment for running the adaptive application on this platform.")
            case Deployment.NATIVE:
                logging.info("INFO: Forcing to setup a native python environment for running the adaptive application on this platform.")
            case Deployment.CONTAINER:
                logging.info("INFO: Forcing to setup containerized environment for running the adaptive application on this platform.")
            case _:
                logging.warning("Unknown deployment type.")

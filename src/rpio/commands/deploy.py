import logging
import sys
import click
import subprocess

from rpio.utils.exit import ExitCode


@click.group()
@click.pass_context
def deploy_cmds():
    pass


@deploy_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def deploy(verbose: bool):
    """Deploy the standalone RoboSAPIENS Adaptive Platform application package on the target."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug("Deploy command under construction")
    run_file = "Realization/ManagingSystem/Actions/deploy.py"
    logger.debug(run_file)

    try:
        subprocess.run(["py.exe", run_file])
    except:
        logger.fatal("FAIL - deploying standalone robosapiensIO application failed")
        sys.exit(ExitCode.FAILURE)

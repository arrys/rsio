import logging
import sys
import click
import subprocess

from rsio.utils.exit import ExitCode


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
    run_file = "Realization/ManagingSystem/Actions/deploy.py" # TODO Whys is this hardcoded?
    logger.debug(run_file)

    try:
        result = subprocess.run([sys.executable, run_file], capture_output=True, text=True)
        if result.returncode != 0:
            logger.fatal(result.stdout)
            sys.exit(ExitCode.FAILURE)
    except (FileNotFoundError, subprocess.SubprocessError, OSError) as e:
        logger.fatal("FAIL - deploying standalone robosapiensIO application failed")
        sys.exit(ExitCode.FAILURE)

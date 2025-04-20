import logging
import sys
import click
import subprocess

from rsio.utils.exit import ExitCode


@click.group()
@click.pass_context
def build_cmds():
    pass


@build_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def build(verbose: bool):
    """Build the standalone RoboSAPIENS Adaptive Platform application package."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    logging.debug("Build command under construction")
    run_file = "Realization/ManagingSystem/Actions/build.py"
    logging.debug(run_file)

    try:
        subprocess.run(["py.exe", run_file])
    except:
        logging.fatal("FAIL - building standalone robosapiensIO application failed")
        sys.exit(ExitCode.FAILURE)

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
    logger.debug("Build command under construction")
    run_file = "Realization/ManagingSystem/Actions/build.py" # TODO Whys is this hardcoded?
    logger.debug(run_file)

    try:
        result = subprocess.run([sys.executable, run_file], capture_output=True, text=True)
        if result.returncode != 0:
            logger.fatal(result.stdout)
            sys.exit(ExitCode.FAILURE)
    except (FileNotFoundError, subprocess.SubprocessError, OSError) as e:
        logger.fatal("FAIL - building standalone robosapiensIO application failed")
        sys.exit(ExitCode.FAILURE)

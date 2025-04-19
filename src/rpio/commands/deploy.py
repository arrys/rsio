import logging
import click
import subprocess


@click.group()
@click.pass_context
def deploy_cmds():
    pass


@deploy_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def deploy(verbose: bool):
    """Deploying the standalone RoboSAPIENS Adaptive Platform application package on target."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug("Deploy command under construction")

    run_file = "Realization/ManagingSystem/Actions/deploy.py"
    arguments = ""
    logger.debug(run_file)

    try:
        subprocess.run(["py.exe", run_file, arguments])
    except:
        logger.fatal("FAIL - deploying standalone robosapiensIO application failed")

import logging
import sys

import click
from rpio.package.manager import PackageManager
from rpio.utils.exit import ExitCode


@click.group()
@click.pass_context
def package_cmds():
    pass


@package_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--check", "-c", is_flag=True, default=False, help="Check if standalone robosapiensIO package is valid.")
@click.option("--create", is_flag=True, default=False, help="Create new standalone robosapiensIO package.")
@click.option("--name", "-n", default="project", help="Name of the new standalone robosapiensIO package [default:'project'].")
def package(verbose: bool, check: bool, create: bool, name: str):
    """Check correctness of standalone robosapiensIO application package."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    logging.debug("Checking the standalone robosapiensIO application package")

    if check and create:
        raise click.UsageError("Options --check and --create are mutually exclusive.")

    package_manager = PackageManager(verbose=verbose)

    if create:
        package_manager.create(name=name, standalone=True)
        sys.exit(ExitCode.SUCCESS)

    if check:
        if package_manager.check():
            logging.info("SUCCESS - Valid robosapiensIO application package")
        else:
            logging.info("FAIL - Invalid robosapiensIO application package")
        sys.exit(ExitCode.SUCCESS) # SUCCESS because the app performs successfully


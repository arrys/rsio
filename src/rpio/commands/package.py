import logging
import click
from rpio.package.manager import PackageManager


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
    if verbose:
        print(logger.level)

    # TODO fix this as it's weird to have two flag with elifs
    if check:
        m = PackageManager(verbose=verbose)
        is_valid = m.check(path=None)

        if is_valid:
            logging.info("SUCCESS - Valid robosapiensIO application package")
        else:
            logging.error("FAIL - Invalid robosapiensIO application package")
    elif create:
        m = PackageManager(verbose=verbose)
        m.create(name=name, standalone=True, path=None)

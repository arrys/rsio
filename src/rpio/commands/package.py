import click
from rpio.package.manager import *


@click.group()
@click.pass_context
def package_cmds():
    pass


@package_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--check", "-c", is_flag=True, default=False, help="Check if standalone robosapiensIO package is valid.")
@click.option("--create", is_flag=True, default=False, help="Create new standalone robosapiensIO package.")
@click.option("--name", "-n", default="project", help="Name of the new standalone robosapiensIO package [default:'project'].")
def package(verbose, check, create, name):
    """Check correctness of standalone robosapiensIO application package."""
    if verbose: print("Checking the standalone robosapiensIO application package")

    if check:
        m = PackageManager(verbose=verbose)
        is_valid = m.check(path=None)

        if is_valid:
            print("SUCCESS - Valid robosapiensIO application package")
        else:
            print("FAIL - Invalid robosapiensIO application package")

    elif create:
        m = PackageManager(verbose=verbose)
        m.create(name=name, standalone=True, path=None)

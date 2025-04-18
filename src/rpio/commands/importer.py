import click


@click.group()
@click.pass_context
def import_cmds():
    pass


@import_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--generate", "-g", is_flag=True, default=False, help="Generate standalone packages.")
@click.option("--RAADL", default="default.raadl", help="Input RAADL models.")
def importer(verbose):
    """Import standalone RoboSAPIENS Adaptive Platform application package."""
    if verbose: print("Importing the standalone robosapiensIO application package")

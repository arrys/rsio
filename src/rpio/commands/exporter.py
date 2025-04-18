import click


@click.group()
@click.pass_context
def exportCmds():
    pass


@exportCmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def exporter(verbose):
    """Export as standalone RoboSAPIENS Adaptive Platform application package."""
    if verbose: print("Exporting the raa package as standalone application package")

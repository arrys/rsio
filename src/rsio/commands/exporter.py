import logging
import click


@click.group()
@click.pass_context
def export_cmds():
    pass


@export_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def exporter(verbose: bool):
    """Export as a standalone RoboSAPIENS Adaptive Platform application package."""
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)
    logging.debug("Exporting the raa package as standalone application package")

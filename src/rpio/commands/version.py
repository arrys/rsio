import click


@click.group()
@click.pass_context
def versionCmds():
    pass

@versionCmds.command()
def version():
    """Display the current version."""
    version = "0.3.24" # TODO Get from pyproject
    click.echo("rpio v"+version)

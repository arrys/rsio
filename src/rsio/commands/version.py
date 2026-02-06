import click
from pathlib import Path
from arkfast import get_project_metadata

@click.group()
@click.pass_context
def version_commands():
    pass


@version_commands.command()
def version():
    """Display the current version."""
    root_project_directory = Path(__file__).resolve().parent.parent.parent
    title, project_version = get_project_metadata(root_project_directory)
    click.echo(f"rsio v{project_version}")

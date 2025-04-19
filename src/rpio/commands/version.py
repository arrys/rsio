import click
import tomllib
from pathlib import Path

@click.group()
@click.pass_context
def version_commands():
    pass


@version_commands.command()
def version():
    """Display the current version."""
    # TODO Check if this works on an installed package
    try:
        data = tomllib.loads((Path(__file__).resolve().parent.parent.parent.parent / Path("pyproject.toml")).read_text())
    except FileNotFoundError:
        data = {}
    project_version = data.get("project", {}).get("version", "0.0.0")
    click.echo(f"rpio v{project_version}")

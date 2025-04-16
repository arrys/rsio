import click

from rpio.commands.version import versionCmds
from rpio.commands.importer import importCmds
from rpio.commands.exporter import exportCmds
from rpio.commands.run import runCmds
from rpio.commands.build import buildCmds
from rpio.commands.package import packageCmds
from rpio.commands.deploy import deployCmds
from rpio.commands.transformations import transformationCmds
from rpio.commands.platform import platformCmds

cli = click.CommandCollection(
    sources=[versionCmds, packageCmds, transformationCmds, runCmds, buildCmds, deployCmds, platformCmds],
    help="robosapiensIO command line tool"
)


def main():
    cli()


if __name__ == "__main__":
    main()

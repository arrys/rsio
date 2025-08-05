import click

from rsio.commands.version import version_commands
from rsio.commands.run import run_cmds
from rsio.commands.build import build_cmds
from rsio.commands.package import package_cmds
from rsio.commands.deploy import deploy_cmds
from rsio.commands.transformations import transformation_cmds
from rsio.commands.platform import platform_cmds

cli = click.CommandCollection(
    sources=[version_commands, package_cmds, transformation_cmds, run_cmds, build_cmds, deploy_cmds, platform_cmds],
    help="robosapiensIO command line tool"
)


def main():
    cli()


if __name__ == "__main__":
    main()

import logging
import arklog
import click

from rpio.commands.version import version_commands
from rpio.commands.run import run_cmds
from rpio.commands.build import build_cmds
from rpio.commands.package import package_cmds
from rpio.commands.deploy import deploy_cmds
from rpio.commands.transformations import transformation_cmds
from rpio.commands.platform import platform_cmds

cli = click.CommandCollection(
    sources=[version_commands, package_cmds, transformation_cmds, run_cmds, build_cmds, deploy_cmds, platform_cmds],
    help="robosapiensIO command line tool"
)


def main():
    cli()


if __name__ == "__main__":
    main()

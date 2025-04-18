import click
import os
import subprocess


@click.group()
@click.pass_context
def build_cmds():
    pass


@build_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def build(verbose):
    """Build standalone RoboSAPIENS Adaptive Platform application package."""
    if verbose: print("Build command under construction")

    _directory = os.getcwd()
    run_file = "Realization/ManagingSystem/Actions/build.py"
    arguments = ""
    if verbose: print(run_file)

    try:
        subprocess.run(["py.exe", run_file, arguments])
    except:
        print("FAIL - building standalone robosapiensIO application failed")

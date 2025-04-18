import click
import os
import subprocess


@click.group()
@click.pass_context
def deploy_cmds():
    pass


@deploy_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
def deploy(verbose):
    """Deploying standalone RoboSAPIENS Adaptive Platform application package on target."""
    if verbose: print("Deploy command under construction")

    _directory = os.getcwd()
    run_file = "Realization/ManagingSystem/Actions/deploy.py"
    arguments = ""
    if verbose: print(run_file)

    try:
        subprocess.run(["py.exe", run_file, arguments])
    except:
        print("FAIL - deploying standalone robosapiensIO application failed")

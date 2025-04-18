import click
import os
import subprocess
from rpio.launcher.launcher import launch, launch_main, launch_docker_compose


@click.group()
@click.pass_context
def run_cmds():
    pass


@run_cmds.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help="Enable debug information.")
@click.option("--platform", "-p", default="none", help="Specify on which platform you want to run the adaptive application, based on the AADL deployment.")
@click.option("--launchfile", is_flag=True, default=False, help="Specify the use of the launchfile to run the adaptive application.")
@click.option("--docker", is_flag=True, default=False, help="Specify the use of docker to run the adaptive application.")
def run(verbose, platform, launchfile, docker):
    """Run standalone RoboSAPIENS Adaptive Platform application package."""
    if verbose: print("Run command under construction...")

    if platform is None:
        if verbose: print("Executing the run.py action (Realization/ManagingSystem/Actions/run.py)")
        _directory = os.getcwd()
        run_file = "Realization/ManagingSystem/Actions/run.py"
        arguments = ""
        if verbose: print(run_file)

        try:
            subprocess.run(["py.exe", run_file, arguments])
        except:
            print("FAIL - Running standalone robosapiensIO application failed")
    else:
        if docker:
            if verbose: print(
                "Executing the adaptive application using the provided docker compose file for platform {}".format(platform))
            try:
                launch_docker_compose(path="Realization/ManagingSystem/Platform/" + platform)
            except:
                print("FAIL - Launching the standalone robosapiensIO application failed")
        elif launchfile:
            if verbose: print(
                "Executing the adaptive application using the provided launch file for platform {}".format(platform))
            try:
                launch("Realization/ManagingSystem/Platform/" + platform + "/launch.xml")
            except:
                print("FAIL - Launching the standalone robosapiensIO application failed")
        else:
            if verbose: print(
                "Executing the adaptive application using the provided main file for platform {}".format(platform))
            try:
                launch_main("Resources/main_" + platform + ".py")
            except:
                print("FAIL - Launching the standalone robosapiensIO application failed")

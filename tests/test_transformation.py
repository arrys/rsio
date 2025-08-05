from pathlib import Path

import rsio.package.manager
import rsio.parsers.parsers
from rsio.metamodels.aadl2il import System
from rsio.transformations.transformations import robochart2aadlmessages
from tests.utils import TemporaryTemplatedPath


def test_aadl_to_aadlil_transformation():
    """"""
    package_manager = rsio.package.manager.PackageManager()
    # TODO Needs better testing with better package input
    with TemporaryTemplatedPath(Path(__file__).resolve().parent / Path("data/ntnu-package.zip"), Path.cwd() / "package") as package_path:
        package_manager.create(package_path.stem, standalone=True)
        # aadl -> aadlil
        rsio.parsers.parsers.AadlParser(
            logical_architecture=package_path / "Design/logicalArchitecture.aadl",
            physical_architecture=package_path / "Design/physicalArchitecture.aadl",
            messages=package_path / "Design/messages.aadl"
        ).aadl2aadl_il().object2json(package_path / "Design/design.json")
        assert (package_path / "Design/design.json").is_file()



def test_aadl_to_aadlil_transformation_reload():
    with TemporaryTemplatedPath(Path(__file__).resolve().parent / Path("data/aadl_to_aadlil.zip"), Path.cwd() / "package") as package_path:
        rsio.parsers.parsers.AadlParser(
            logical_architecture= package_path / "logicalArchitecture.aadl",
            physical_architecture= package_path/ "PhysicalArchitecture.aadl",
            messages= package_path / "messages.aadl"
        ).aadl2aadl_il().object2json(file_name=package_path / "system.json")
        loaded_system = System(name="adaptiveSystem", description="Generated from AADL models", json_descriptor=package_path / "system.json")
        loaded_system.object2json(file_name=package_path / "loaded.json")


# def test_robochart_to_aadl_transformation():
#     parser = rpio.RobochartParser(
#         maplek='input/MAPLE-K.rct',
#         monitor='input/Monitor.rct',
#         analysis='input/Analysis.rct',
#         plan='input/Plan.rct',
#         legitimate='input/Legitimate.rct',
#         execute='input/Execute.rct',
#         knowledge='input/Knowledge.rct'
#     )
#     x = robochart2aadlmessages(maplek=parser.maplek_model,path='output/')


# def test_aadl_to_py_transformation():
#     """"""
#     from rpio.transformations.transformations import swc2code_py,message2code_py
#     from rpio.metamodels.aadl2il.examples.example1 import example
#
#     system = example()
#     x=1
#     try:
#         message2code_py(system=system, path="output/generated/messages")
#         swc2code_py(system=system,path="output/generated")
#     except:
#         print("Failed to generate")

from pathlib import Path

import rpio.package.manager
import rpio.parsers.parsers
from tests.utils import TemporaryTemplatedPath


def test_aadl_to_aadlil_transformation():
    """"""
    package_manager = rpio.package.manager.PackageManager()
    package_name = "package"
    # TODO Needs better testing with better package input
    with TemporaryTemplatedPath(Path(__file__).resolve().parent / Path("data/ntnu-package.zip"), package_name) as package_path:
        package_manager.create(package_name, standalone=True)
        # aadl -> aadlil
        rpio.parsers.parsers.AADL_parser(
            logicalArchitecture=str(package_path / "Design/logicalArchitecture.aadl"),
            physicalArchitecture=str(package_path / "Design/physicalArchitecture.aadl"),
            messages=str(package_path / "Design/messages.aadl")
        ).aadl2aadlIl().object2json(fileName=str(package_path / "Design/design.json"))
        assert (package_path / "Design/design.json").is_file()

# def test_aadl_to_py_transformation():
#     """"""
#     from rpio.transformations.transformations import swc2code_py,message2code_py
#     from rpio.metamodels.aadl2_IL.examples.example1 import example
#
#     system = example()
#     x=1
#     try:
#         message2code_py(system=system, path="output/generated/messages")
#         swc2code_py(system=system,path="output/generated")
#     except:
#         print("Failed to generate")

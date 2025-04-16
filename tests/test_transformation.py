from pathlib import Path

import rpio.package.manager
import rpio.parsers.parsers
from tests.utils import TemporaryTemplatedPath


def test_aadl_to_aadlil_transformation():
    """"""
    package_manager = rpio.package.manager.PackageManager()
    package_name = "package"
    # TODO Needs better testing with better package input
    with TemporaryTemplatedPath(Path("data/ntnu-package.zip"), package_name) as package_path:
        package_manager.create(package_name, standalone=True)
        # aadl -> aadlil
        rpio.parsers.parsers.AADL_parser(
            logicalArchitecture=str(package_path / "Design/logicalArchitecture.aadl"),
            physicalArchitecture=str(package_path / "Design/physicalArchitecture.aadl"),
            messages=str(package_path / "Design/messages.aadl")
        ).aadl2aadlIl().object2json(fileName=str(package_path / "Design/design.json"))
        assert (package_path / "Design/design.json").is_file()

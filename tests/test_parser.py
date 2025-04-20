from pathlib import Path

from rsio.metamodels.aadl2il import System
from tests.utils import TemporaryTemplatedPath


def test_aadlil_parser():
    with TemporaryTemplatedPath(Path(__file__).resolve().parent / Path("data/parser.zip"), Path.cwd() / "package", False) as package_path:
        loaded_system = System(name="adaptiveSystem", description="Loaded from aadlil", json_descriptor=package_path / "aadlil.json")
        assert loaded_system.name == "adaptiveSystem"

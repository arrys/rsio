from pathlib import Path
from rpio.launcher.launcher import launch
from tests.utils import TemporaryTemplatedPath


# def test_launch():
#     with TemporaryTemplatedPath(Path(__file__).resolve().parent / Path("data/hell0.zip"), Path.cwd() / "package", False) as package_path:
#         launch(package_path / "launch.xml")

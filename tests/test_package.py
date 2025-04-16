import rpio.package.manager
from tests.utils import TemporaryPath


def test_package():
    """"""
    package_manager = rpio.package.manager.PackageManager()

    package_name = "package"
    with TemporaryPath(package_name) as package_path:
        # package_manager.create(package_name, path=package_path, standalone=True) # TODO Passing in a path breaks the manager
        package_manager.create(package_name, standalone=True)
        assert package_path.is_dir()
        assert (package_path / "Realization/ManagedSystem/Actions/deploy.py").is_file() # Random spotcheck
        assert package_manager.check(str(package_path))
        assert package_manager.check(package_path)

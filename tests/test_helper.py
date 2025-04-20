import logging
from pathlib import Path

import pytest

from rsio.utils.auxiliary import is_python_package_installed, is_mqtt_reachable, is_redis_reachable, get_docker_version, \
    run_docker_container, build_docker_image, get_python_version, install_python_packages_from_requirements_file


def test_deactivate_virtual_environment(caplog):
    pass

def test_install_python_packages_from_requirements_file(caplog):
    with pytest.raises(FileNotFoundError):
        install_python_packages_from_requirements_file(Path("nonexistent/requirements.txt"))

def test_get_python_version(caplog):
    version = get_python_version()
    assert isinstance(version, str)
    parts = version.split(".")
    assert len(parts) == 3

def test_build_docker_container(caplog):
    # NOTE: Depends on something installed on the host machine
    with pytest.raises(FileNotFoundError):
        build_docker_image(Path("nonexistent/Dockerfile"), "name")
    # with caplog.at_level(logging.DEBUG):
    #     command_successful = build_docker_image(Path("Dockerfile"), "name")
    #     assert isinstance(command_successful, bool)
    #     assert len(caplog.text) > 0

def test_run_docker_container(caplog):
    # NOTE: Depends on something installed on the host machine
    with caplog.at_level(logging.DEBUG):
        command_successful = run_docker_container("hello-world", "name", {5000: 5000})
        assert isinstance(command_successful, bool)
        assert len(caplog.text) > 0

def test_docker_version_check(caplog):
    version = get_docker_version()
    assert isinstance(version, str) or version == False

@pytest.mark.long
def test_redis_reachable_check(caplog):
    # NOTE: Depends on something installed on the host machine
    assert is_redis_reachable() is False

@pytest.mark.long
def test_mqtt_reachable_check(caplog):
    # NOTE: Depends on something installed on the host machine
    assert is_mqtt_reachable() is False

def test_python_package_installation_check(caplog):
    assert is_python_package_installed("not_existing_package") is False
    assert is_python_package_installed("rsio") is True

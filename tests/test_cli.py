import logging

import pytest
from click.testing import CliRunner
from rsio.__main__ import cli
from rsio.utils.exit import ExitCode
from tests.utils import TemporaryPath

def test_cli_launch():
    result = CliRunner().invoke(cli)
    #assert result.exit_code == ExitCode.SUCCESS
    output = result.output
    assert "Usage:" in output
    assert "Commands:" in output

def test_cli_build(caplog):
    runner = CliRunner()
    command = "build"
    result = runner.invoke(cli, [command])
    assert result.exit_code == ExitCode.FAILURE

def test_cli_deploy(caplog):
    runner = CliRunner()
    command = "deploy"
    result = runner.invoke(cli, [command])
    assert result.exit_code == ExitCode.FAILURE

def test_cli_export(caplog):
    runner = CliRunner()
    command = "export"
    result = runner.invoke(cli, [command])

def test_cli_import(caplog):
    runner = CliRunner()
    command = "import"
    result = runner.invoke(cli, [command])

def test_cli_package(caplog):
    runner = CliRunner()
    command = "package"
    result = runner.invoke(cli, [command])
    assert result.exit_code == ExitCode.SUCCESS

    with caplog.at_level(logging.DEBUG):
        result = runner.invoke(cli, [command, "--check"])
        assert result.exit_code == ExitCode.SUCCESS
        assert "FAIL" in caplog.text

        result = runner.invoke(cli, [command, "--verbose"])
        assert result.exit_code == ExitCode.SUCCESS
        assert "Checking" in caplog.text

        package_name = command
        with TemporaryPath(package_name):
            result = runner.invoke(cli, [command, "--verbose", "--create", "--name", package_name])
            assert result.exit_code == ExitCode.SUCCESS
            # assert "package created" in result.output
            assert "package created" in caplog.text

@pytest.mark.long
def test_cli_platform(caplog):
    runner = CliRunner()
    command = "platform"
    result = runner.invoke(cli, [command, "--verbose"])
    result = runner.invoke(cli, [command, "--verbose", "--check"])
    result = runner.invoke(cli, [command, "--verbose", "--set"])
    result = runner.invoke(cli, [command, "--verbose", "--name"])
    result = runner.invoke(cli, [command, "--verbose", "--force"])


def test_cli_transformation():
    command = "transformation"
    runner = CliRunner()
    # TODO The roboarch2aadl transformation is not implemented at the moment
    result = runner.invoke(cli, [command, "--roboarch2aadl"])
    assert result.exit_code == ExitCode.SUCCESS

def test_cli_version():
    command = "version"
    runner = CliRunner()
    result = runner.invoke(cli, [command])
    assert "rsio v" in result.output
    assert result.exit_code == ExitCode.SUCCESS

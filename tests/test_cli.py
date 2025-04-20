import logging

from click.testing import CliRunner
from rpio.__main__ import cli
from tests.utils import TemporaryPath

def test_cli_launch():
    """"""
    result = CliRunner().invoke(cli)
    assert result.exit_code == 0
    output = result.output
    assert "Usage:" in output
    assert "Commands:" in output

def test_cli_package(caplog):
    """"""
    runner = CliRunner()
    command = "package"
    result = runner.invoke(cli, [command])
    assert result.exit_code == 0

    with caplog.at_level(logging.DEBUG):
        result = runner.invoke(cli, [command, "--check"])
        assert result.exit_code == 0
        assert "FAIL" in caplog.text

        result = runner.invoke(cli, [command, "--verbose"])
        assert result.exit_code == 0
        assert "Checking" in caplog.text

        package_name = command
        with TemporaryPath(package_name):
            result = runner.invoke(cli, [command, "--verbose", "--create", "--name", package_name])
            assert result.exit_code == 0
            # assert "package created" in result.output
            assert "package created" in caplog.text

def test_cli_transformation():
    """"""
    command = "transformation"
    runner = CliRunner()
    # TODO The roboarch2aadl transformation is not implemented at the moment
    result = runner.invoke(cli, [command, "--roboarch2aadl"])
    assert result.exit_code == 0

def test_cli_version():
    """"""
    command = "version"
    runner = CliRunner()
    result = runner.invoke(cli, [command])
    assert  "rpio v" in result.output

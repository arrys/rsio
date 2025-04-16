from click.testing import CliRunner
from rpio.__main__ import cli
from utils import TemporaryPath

def test_cli_launch():
    """"""
    result = CliRunner().invoke(cli)
    assert result.exit_code == 0 # TODO This should not be 0
    output = result.output
    assert "Usage:" in output
    assert "Commands:" in output

def test_cli_package():
    """"""
    runner = CliRunner()
    command = "package"
    result = runner.invoke(cli, [command])
    assert result.exit_code == 0  # TODO This should not be 0

    result = runner.invoke(cli, [command, "--check"])
    assert result.exit_code == 0  # TODO This should not be 0
    assert "FAIL" in result.output

    result = runner.invoke(cli, [command, "--verbose"])
    assert result.exit_code == 0  # TODO This should not be 0
    assert "Checking" in result.output

    package_name = command
    with TemporaryPath(package_name):
        result = runner.invoke(cli, [command, "--verbose", "--create", "--name", package_name])
        assert result.exit_code == 0
        assert "package created" in result.output

def test_cli_transformation():
    """"""
    command = "transformation"
    runner = CliRunner()
    # TODO The roboarch2aadl transformation is not implemented at the moment
    result = runner.invoke(cli, [command, "--roboarch2aadl"])
    assert result.exit_code == 0  # TODO This should not be 0

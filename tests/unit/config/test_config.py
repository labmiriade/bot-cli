from click.testing import CliRunner

from src.main import cli


def test_config_is_enabled():
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "--help"])
    # the command exists and returns cleanly
    assert result.exit_code == 0

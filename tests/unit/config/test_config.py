from click.testing import CliRunner

from src.config.config import config
from src.main import cli


def test_config_is_enabled():
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "--help"], catch_exceptions=False)
    # the command exists and returns cleanly
    assert result.exit_code == 0


def test_config_has_keywords():
    runner = CliRunner()
    result = runner.invoke(config)
    # the command output contains the following parameters
    assert "username" in result.output
    assert "password" in result.output
    assert "sede" in result.output or "ufficio" in result.output
    assert "~/.mirbot" in result.output

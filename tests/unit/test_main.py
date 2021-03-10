from click.testing import CliRunner

from src.main import *


def test_cli_has_commands():
    """
    Check that all subcommands exists in the main one
    """
    ctx = object()
    commands = cli.list_commands(ctx)
    assert "rapp" in commands
    assert "settings" in commands
    assert "config" in commands


def test_cli_has_help():
    """
    Check that the --help command exists in bot
    """
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0

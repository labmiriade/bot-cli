#! python

import click

from .cli_utils import load_default_map
from .click.aliased_group import AliasedGroup
from .config.config import config
from .rapportini.main import rapp
from .settings.main import settings

SHORT_HELP_TEXT = """
Command line tool per interagire con BOT 🐷
"""

HELP_TEXT = """
Puoi utilizzare questo tool per effettuare
le attività più comuni effettuate con BOT 🐷
"""


@click.command(help=HELP_TEXT, short_help=SHORT_HELP_TEXT, cls=AliasedGroup)
@click.pass_context
def cli(ctx):
    """
    This is the initial click.Group, here is named `cli` but the name used to call it is different,
    probably `bot`.
    """
    ctx.default_map = load_default_map()


cli.add_command(rapp)
cli.add_command(settings)
cli.add_command(config)

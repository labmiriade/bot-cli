import click

from .add import add
from .ls import ls
from .missing import missing
from .rm import rm
from ..cli_utils import AliasedGroup


@click.group(help='Operazioni sui rapportini', cls=AliasedGroup)
def rapp():
    """
    The group for holding commands on rapportini
    """
    pass


rapp.add_command(add)
rapp.add_command(ls)
rapp.add_command(missing)
rapp.add_command(rm)

import click

from .add import add
from .ls import ls
from .missing import missing
from .rm import rm
from ..cli_utils import stored_creds
from ..click.aliased_group import AliasedGroup
from ..repositories.bot import Bot


CREDENTIALS_NOT_SET_1 = """
 🐷 Devi configurare sia username (email) che password per poter
    usare questa funzione. Utilizza il comando:
"""
CREDENTIALS_NOT_SET_2 = "        bot config"
CREDENTIALS_NOT_SET_3 = """
    per configuare un file di configurazione, o imposta le variabili
    BOT_USERNAME e BOT_PASSWORD.
"""


@click.group(help="Operazioni sui rapportini", cls=AliasedGroup)
@click.pass_context
def rapp(ctx):
    """
    The group for holding commands on rapportini
    """
    if ctx.obj is None:
        username, password = stored_creds()
        if username is None or password is None:
            click.secho(CREDENTIALS_NOT_SET_1, fg="red")
            click.secho(CREDENTIALS_NOT_SET_2, fg="cyan")
            click.secho(CREDENTIALS_NOT_SET_3, fg="red")
            exit(1)
        ctx.obj = Bot(username=username, password=password)
    pass


rapp.add_command(add)
rapp.add_command(ls)
rapp.add_command(missing)
rapp.add_command(rm)

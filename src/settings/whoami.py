import click

from ..cli_utils import stored_creds
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


@click.command(help="Mostra informazioni sull'utente")
def whoami():
    """
    This command is useful for debugging problems related to the current user
    """
    username, password = stored_creds()
    if username is None or password is None:
        click.secho(CREDENTIALS_NOT_SET_1, fg="red")
        click.secho(CREDENTIALS_NOT_SET_2, fg="cyan")
        click.secho(CREDENTIALS_NOT_SET_3, fg="red")
        exit(1)
    repo = Bot(username=username, password=password)
    click.echo(f'Ciao {click.style(username, fg="green")}!')
    user_id, res_id = repo.user_id, repo.res_id
    click.echo(
        f'Il tuo user è {click.style(user_id, fg="yellow")}, '
        f'il tuo resId (o tecnicoId) è {click.style(res_id, fg="yellow")}.'
    )
    click.echo(f'La cache si trova in {click.style(repo.cache.cache_dir, fg="bright_magenta")}')

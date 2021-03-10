#! python

import click
import toml

from src.cli_utils import CredsCommand, config as stored_config, CONFIG_FILE, AliasedGroup
from .rapportini import rapp
from src.rapportini.rapportini_printer import offices_choices
from src.repo import Repo
from src.settings import settings

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
    usually `bot`.
    """
    pass


@cli.command(help='Mostra informazioni sull\'utente', cls=CredsCommand)
@click.pass_context
def whoami(ctx, username, password):
    """
    This command is useful for debugging problems related to the current user
    Args:
        ctx ():
        username (): The username to use
        password (): The password for the user
    """
    click.echo(f'Ciao {click.style(username, fg="green")}!')
    repo = Repo(username, password)
    user_id, res_id = repo.user_id, repo.res_id
    click.echo(f'Il tuo user è {click.style(user_id, fg="yellow")}, '
               f'il tuo resId (o tecnicoId) è {click.style(res_id, fg="yellow")}.')
    click.echo(f'La cache si trova in {click.style(repo.cache.cache_dir, fg="bright_magenta")}')


@cli.command(help='Configura BOT nel terminale')
def config():
    """
    Allows the user to update the saved configurations in the .mirbot toml file
    """
    # read the current values, to present them as defaults
    current_values = stored_config
    click.secho(f' 🐷 Ora ti guiderò nell\'impostazione delle configurazioni principali\n', fg='magenta')

    # Credentials
    #  update username and password
    creds = stored_config.get('creds', {})
    click.secho('Inserisci la tua mail aziendale', fg='green')
    creds['username'] = click.prompt('  username', default=creds.get('username'),
                                     type=click.STRING)
    click.echo('')  # add a newline char
    click.secho('Inserisci la tua password, se non la conosci perché entri', fg='cyan')
    click.secho('sempre con Google clicca su "password dimenticata" in homepage', fg='cyan')
    creds['password'] = click.prompt('  password', default=creds.get('password'),
                                     hide_input=True, type=click.STRING)
    click.echo('')  # add a newline char
    # if the user enters a space, remove the associated value in config
    if creds['username'].strip() == '':
        creds['username'] = None
    if creds['password'].strip() == '':
        creds['password'] = None
    current_values['creds'] = creds

    # Rapp
    #  default office
    rapp = current_values.get('rapp', {})
    click.secho('Impostiamo ora l\'ufficio di default per i nuovi rapportini\n(potrai comunque cambiarlo ogni volta)',
                fg='bright_magenta')
    click.secho('Le sedi sono:', fg='bright_magenta')
    for office in offices_choices:
        click.secho(f'  - {office}', fg='bright_magenta')
    click.secho(f'Basta indicare il numero della relativa sede', fg='bright_magenta')
    rapp['office'] = click.prompt('  sede', default=rapp.get('office'), type=click.STRING)
    if rapp['office'].strip() == '':
        rapp['office'] = None
    current_values['rapp'] = rapp
    click.echo('')  # add a newline char

    # Override the toml config file
    with open(CONFIG_FILE, 'w') as f:
        toml.dump(current_values, f)

    click.secho(f' 🐷 Finito! se vuoi modificare il file manualmente, lo trovi in ~/.mirbot', fg='magenta')


cli.add_command(rapp)
cli.add_command(settings)
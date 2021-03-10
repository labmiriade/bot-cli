import click

from src.cli_utils import CredsCommand
from src.bot import Bot


@click.command(help="Mostra informazioni sull'utente", cls=CredsCommand)
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
    repo = Bot(username, password)
    user_id, res_id = repo.user_id, repo.res_id
    click.echo(
        f'Il tuo user è {click.style(user_id, fg="yellow")}, '
        f'il tuo resId (o tecnicoId) è {click.style(res_id, fg="yellow")}.'
    )
    click.echo(f'La cache si trova in {click.style(repo.cache.cache_dir, fg="bright_magenta")}')

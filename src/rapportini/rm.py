import click

from .rapportini_printer import deleted_rapp
from ..cli_utils import CredsCommand
from ..bot import Bot


@click.command(help="Elimina uno o più rapportini", cls=CredsCommand)
@click.argument("id_rapportini", nargs=-1)
@click.pass_obj
def rm(repo, username, password, id_rapportini):
    repo = Bot(username, password)
    printer = deleted_rapp()
    deleted_count = 0
    for i in id_rapportini:
        r = repo.delete_rapportino(i)
        if r is None:
            click.echo(f" impossibile eliminare {click.style(i, fg='yellow')}")
        else:
            commessa = (repo.get_commessa(job_id=r["jobId"]) or {}).get("description", r["jobId"])
            printer(r, str(commessa))
            deleted_count = deleted_count + 1
        click.echo("", nl=True)
    countable = "il rapportino" if deleted_count == 1 else f"{deleted_count} rapportini"
    click.secho(f" 🐷 Ho eliminato {countable} su {len(id_rapportini)}!", fg="magenta")

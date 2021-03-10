from typing import List

import click

from ..cli_utils import CredsCommand
from ..repo import Repo, MissingRapportino
from ..utils import datefromt


@click.command(help="Mostra i raportini mancanti", cls=CredsCommand)
@click.pass_obj
def missing(repo, username, password):
    repo = Repo(username, password)
    rapps: List[MissingRapportino] = repo.get_missing()
    if len(rapps) == 0:
        click.secho(" 🐷 Complimenti, hai inserito tutti i rapportini!", fg="magenta")
    else:
        click.secho("      Data       |  Ore già inserite")
        click.secho("-----------------+--------------------")
        rapps.reverse()
        for m in rapps:
            d = datefromt(m["date"])
            h = m["oreGiornoRegistrate"]
            click.secho(f' {d.strftime("%a %d-%m-%Y")} ', fg="green", nl=False)
            click.secho(" | ", nl=False)
            click.secho(f" {h} ", fg="bright_blue", nl=True)

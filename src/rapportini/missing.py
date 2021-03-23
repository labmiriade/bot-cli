from typing import List

import click

from ..repositories.bot import MissingRapportino
from ..repositories.events_printer import short_printer
from ..repositories.google import get_events_on, has_google_credentials
from ..utils import datefromt


@click.command(help="Mostra i raportini mancanti")
@click.option(
    "--use-calendar/--no-use-calendar",
    "with_calendar",
    default=has_google_credentials,
    help="mostra gli eventi da calendar per i giorni in cui mancano rapportini",
)
@click.pass_context
def missing(ctx, with_calendar: bool):
    bot = ctx.obj
    rapps: List[MissingRapportino] = bot.get_missing()
    if len(rapps) == 0:
        click.secho(" 🐷 Complimenti, hai inserito tutti i rapportini!", fg="magenta")
    elif with_calendar:
        click.secho("  Giorni mancanti  ")
        click.secho("============================================================================")
        rapps.reverse()
        for m in rapps:
            d = datefromt(m["date"])
            h = m["oreGiornoRegistrate"]
            events = get_events_on(d)
            click.secho(f' {d.strftime("%a %d-%m-%Y")} ', fg="green", nl=False)
            click.secho(" | ", nl=False)
            click.secho(f" {h} ", fg="yellow", nl=True)
            if events:
                printer = short_printer(date=d, indent=3, max_length=ctx.max_content_width)
                for e in events:
                    printer(e)
            else:
                click.secho("     Non ci sono eventi a calendario")
            click.echo("")
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

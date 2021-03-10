import datetime
from typing import Optional

import click

from .rapportini_printer import full_rapp, short_rapp


@click.command(help="Mostra i rapportini inseriti")
@click.option(
    "-d",
    "--data",
    type=click.DateTime(formats=["%Y-%m-%d", "%d-%m-%Y", "%d-%m"]),
    default=None,
    help="La data per cui va inserito il rapportino",
)
@click.option(
    "-c", "--count", type=click.IntRange(1, 14, clamp=False), help="Quanti giorni mostrare", show_default=False
)
@click.option(
    "-f",
    "--format",
    "fmt",
    type=click.Choice(["short", "full"]),
    help="Quanti dettagli vuoi sui rapportini",
    default="short",
    show_default=True,
)
@click.pass_obj
def ls(repo, data: datetime.datetime, count: Optional[int], fmt: str):
    if data is not None:
        data = data.replace(tzinfo=datetime.timezone.utc)
        count = count or 1
    else:
        data = datetime.datetime.now(tz=datetime.timezone.utc)
        data = data.replace(hour=0, minute=0, second=0, microsecond=0)
        count = count or 7
    missing_dates = set(map(lambda x: str(x["date"]), repo.get_missing()))
    if fmt == "full":
        printer = full_rapp(indents=4, hide_date=True)
    else:
        printer = short_rapp(indents=2, hide_date=True)
    while count > 0:
        count -= 1
        timestamp = int(data.timestamp()) * 1000
        # check if the date has missing rapportini
        has_missing_rapportini = str(timestamp) in missing_dates
        # get the rapportini for the day
        rapportini = repo.get_rapportini(timestamp)
        # print the header
        click.secho(f' {data.strftime("%a %Y-%m-%d")}:', fg="green", nl=False)
        click.secho(f" {len(rapportini)} rapportini", fg="cyan", nl=False)
        total_hours = 0
        for r in rapportini:
            total_hours += r["quantityHours"]
            total_hours += r["quantityMinutes"] / 60
        click.secho(
            f" {total_hours} ore",
            fg="bright_red" if has_missing_rapportini else "bright_cyan",
            nl=True,
            blink=has_missing_rapportini,
        )
        # iterate through the rapportini
        for i, r in enumerate(rapportini):
            # print it
            printer(r)
            # print the separator among rapportini
            if i < len(rapportini) - 1 and fmt == "full":
                click.secho(f"    ----------------------------------------")
        if count > 0:
            # if there are more dates, print a separator
            if fmt == "full":
                click.secho(f"============================================")
            else:
                click.secho(f"--------------------------------------------")
        # decrease the date by one day
        data = data - datetime.timedelta(days=1)

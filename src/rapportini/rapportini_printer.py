from typing import Optional, List, Callable

import click

from ..bot import Rapportino, DeletedRapportino
from ..utils import datefromt

# The offices allowed choices
offices_choices: List[str] = [
    "2_Thiene",
    "1_Padova",
    "3_AZero",
    "4_RVE",
    "5_Formazione",
    "6_Casa",
    "7_Cliente",
    "8_Cliente_no_pranzo",
    "9_Cliente_maggiorazione",
]


def hour(h: int, m: int) -> str:
    """
    Format hours and minutes the right way
    Args:
        h (int): the number of hour
        m (int): the number of minutes

    Returns:
        (str): a text representing the inputed hours and minutes
    """
    return f'{h}:{m if m >= 10 else "0" + str(m)}'


def full_rapp(indents: int = 1, hide_date: bool = False) -> Callable[[Rapportino], None]:
    ind = " " * indents

    def printer(r: Rapportino):
        # format the date
        d = datefromt(r["date"]).strftime("%a %d-%m-%Y")
        # format the hour
        h = hour(r["quantityHours"], r["quantityMinutes"])
        # format the office
        offices = list(filter(lambda x: x.lower().startswith(str(r["officeId"])), offices_choices))
        if len(offices) == 1:
            o = offices[0]
        else:
            o = r["officeId"]

        # the header with date (if not hidden) and hours
        header = "{}{}{}".format(
            click.style(f"{r['rapportinoId']} " if int(r["rapportinoId"]) > 0 else "", fg="green"),
            click.style(f"{d:<12} " if not hide_date else "", fg="green"),
            click.style(f"{h:<35}", fg="yellow"),
        )
        # the title with commessa and attività
        title = click.style(r["commessa"], fg="blue") + " " + click.style(r["attivita"], fg="bright_cyan")
        # the subehad with office and all flags
        subhead = "{}{}{}{}{}".format(
            click.style(f"{o}", fg="bright_magenta"),
            " 🚗" if r["flagTransfert"] else "",
            " 💳" if r["flagPrepay"] else "",
            " 💶" if r["flagPay"] else "",
            " ⏱" if r["flagExtraHour"] else "",
        )
        # the content with the description and eventually the notes
        content = r["description"]
        if r["note"] != "":
            content += click.style(f"\n{ind}---\n{ind}" + r["note"], fg="bright_black")

        # print everything
        click.echo(f"{ind}{header}")
        click.echo(f"{ind}{title}")
        click.echo(f"{ind}{subhead}")
        click.echo(f"{ind}{content}")

    return printer


def short_rapp(indents: int = 1, hide_date: bool = False) -> Callable[[Rapportino], None]:
    ind = " " * indents

    def printer(r: Rapportino):
        click.secho(f"{ind}{r['rapportinoId']:>9} ", fg="yellow", nl=False)
        click.secho(f" {hour(r['quantityHours'], r['quantityMinutes']):>5} ", fg="cyan", nl=False)
        click.secho(f" {r['commessa']} ", fg="bright_green", nl=False)
        click.secho(f" {r['attivita']} ", nl=True)

    return printer


def deleted_rapp(indents: int = 1) -> Callable[[DeletedRapportino, Optional[str]], None]:
    ind = " " * indents

    def printer(r: DeletedRapportino, commessa: Optional[str]):
        click.secho(f"{ind}{r['rapportinoId']} ", fg="yellow", nl=False)
        click.secho(f"{datefromt(r['date']).strftime('%a %d-%m-%Y')}", fg="green", nl=commessa is None)
        if commessa is not None:
            click.secho(f"{ind}{commessa}", fg="cyan", nl=True)
        click.secho(f"{ind}{r['description']}", nl=True)
        if r["note"] != "":
            click.secho(f"{ind}---", fg="bright_black")
            click.secho(f"{ind}{r['note']}", fg="bright_black")

    return printer

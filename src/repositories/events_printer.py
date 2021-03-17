import datetime
from typing import Dict, Iterable, Optional

import click

from src.repositories.google import get_events_on


def short_printer(date: datetime.date, indent: int = 2, max_length: Optional[int] = None):
    ind = " " * indent

    def p(e: Dict):
        # prevent cancelled events to be displayed
        if e["status"] == "cancelled":
            return
        time = click.style(_start_end_time(e, date))
        summary = click.style(e["summary"], fg="cyan")
        click.echo(f"{ind}{time} {summary}")
        attendees = _get_attendees(e)
        if attendees:
            s = ind + "  " + ", ".join(attendees)
            if max_length:
                s = s[:max_length]
            click.secho(s, fg="bright_black")

    return p


def _start_end_time(e: Dict, date: datetime.date) -> str:
    """
    Given an event and the reference date, returns a string describing it start and end time.
    if the event has starttime and endtime print start/end times
    if the event is all day print "all day"
    if the event begins before the date or ends after the date, print accordingly
    """
    all_day = "tutto il giorno"
    # try getting datetimes
    try:
        starttime = datetime.datetime.fromisoformat(e["start"]["dateTime"])
        endtime = datetime.datetime.fromisoformat(e["end"]["dateTime"])
        fmt = "%-H:%M"
        if endtime.date() == date == endtime.date():
            aux = f"{starttime.strftime(fmt)} - {endtime.strftime(fmt)}"
        elif starttime.date() == date < endtime.date():
            aux = f"{starttime.strftime(fmt)} - *"
        elif starttime.date() < date == endtime.date():
            aux = f"* - {endtime.strftime(fmt)}"
        else:
            aux = all_day
        return aux
    except KeyError:
        pass
    # try getting date for all time ones
    return all_day


def _get_attendees(e: Dict) -> Iterable[str]:
    attendees = e.get("attendees", [])
    # remove self from the list
    attendees = filter(lambda x: not x.get("self", False), attendees)
    # remove resources
    attendees = filter(lambda x: not x.get("resource", False), attendees)
    # filter out who did not accepted
    attendees = filter(lambda x: x.get("responseStatus", "unknown") != "declined", attendees)
    # put the organizer as first attendee
    attendees = sorted(attendees, key=lambda x: x.get("organizer", False), reverse=True)
    # for each attendee take the display name or the email
    attendees = [x.get("displayName", x["email"]) for x in attendees]
    return attendees


if __name__ == "__main__":
    d = datetime.date(2021, 3, 5)
    printer = short_printer(d)
    aux = get_events_on(d)
    for event in aux:
        printer(event)

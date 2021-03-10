import datetime
from typing import Union, Tuple, Optional

import click


def datefromt(t: int) -> datetime.date:
    """
    Returns a date object from a unix timestamp (milliseconds from 1970-01-01)
    """
    return datetime.date.fromtimestamp(t / 1000)


def tfromdate(date: datetime.date) -> int:
    """
    Returns the unixtimestamp to be sent to bot for a given date
    """
    dt = datetime.datetime(date.year, date.month, date.day, tzinfo=datetime.timezone.utc)
    return int(dt.timestamp()) * 1000


def merge_id_desc(id: Union[str, int], description: Optional[str]) -> str:
    """
    Returns a string that merges the id and the description in a single string

    This will also replace spaces with underscore
    Args:
        id (Union[str, int]): the id to use
        description (str): the description to merge

    Returns:
        a str with the merged values
    """
    desc = description.strip().replace(" ", "_")
    aux = click.style(str(id), fg="yellow")
    if not desc == "":
        aux += f"_{desc}"
    return aux


def unmerge_id_desc(desc: str) -> Tuple[str, Optional[str]]:
    """
    Undo what has been done by `merge_id_desc` returning the id (first component)
    Args:
        desc (str): the descriptive value (<id>_<description>)

    Returns:
        a tuple composed by a str with the id and a string with the description
    """
    components = str(desc.strip()).split("_")
    fst = components[0]
    snd = " ".join(components[1:]) if len(components) > 1 else None
    return fst, snd


def parse_ore_minuti(s: str) -> Tuple[int, int]:
    """
    Take a string representig hours and minutes and returns the integers.
    Currently 2 formats are supported: `4:30` or `4.5`.
    Args:
        s (str): the inputed value

    Returns:
        a tuple with the hours first and the minutes second
    """
    # strip spaces
    s = s.strip()

    # detect which format is used
    if ":" in s:  # hh:mm
        ss = s.split(":")
        h = int(ss[0])
        m = int(ss[1]) if len(ss) > 1 else 0
    else:  # parse hour only (i.e. 3 or 3.5)
        fh = float(s)
        h = int(fh)
        m = int((fh * 60) % 60)
    return h, m

import datetime
from typing import Union, Tuple

import click


def datefromt(t: int) -> datetime.date:
    return datetime.date.fromtimestamp(t / 1000)


def tfromdate(date: Union[datetime.date, datetime.datetime]) -> int:
    if isinstance(date, datetime.date):
        dt = datetime.datetime(date.year, date.month, date.day)
    else:
        dt = date
    return int(dt.timestamp()) * 1000


def merge_id_desc(id: Union[str, int], description: str) -> str:
    """
    Returns a string that merges the id and the description in a single string

    This will also replace spaces with underscore
    Args:
        id (Union[str, int]): the id to use
        description (str): the description to merge

    Returns:
        a str with the merged values
    """
    return f"{click.style(str(id), fg='yellow')}_{description.strip().replace(' ', '_')}"


def id_from_desc(desc: str) -> str:
    """
    Undo what has been done by `merge_id_desc` returning only the id for the component
    Args:
        desc (str): the descriptive value (<id>_<description>)

    Returns:
        a str with the id
    """
    return str(desc.strip()).split('_')[0]


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
    if ':' in s:  # hh:mm
        ss = s.split(':')
        h = int(ss[0])
        m = int(ss[1]) if len(ss) > 1 else 0
    else:  # parse hour only (i.e. 3 or 3.5)
        fh = float(s)
        h = int(fh)
        m = int((fh * 60) % 60)
    return h, m

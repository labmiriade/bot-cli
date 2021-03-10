import datetime
from typing import Tuple, Union

import click
import pytest

from src.utils import *


@pytest.mark.parametrize(
    ("given", "exp"),
    [
        (1615334400000, datetime.date(2021, 3, 10)),
        (1615161600000, datetime.date(2021, 3, 8)),
        (0, datetime.date(1970, 1, 1)),
    ],
)
def test_datefromt(given: int, exp: datetime.date):
    # WHEN
    d = datefromt(given)
    # EXPECT
    assert d == exp


@pytest.mark.parametrize(
    ("given", "exp"),
    [
        (datetime.date(2021, 3, 10), 1615334400000),
        (datetime.date(2021, 3, 8), 1615161600000),
        (datetime.date(1970, 1, 1), 0),
    ],
)
def test_tfromdate(given: datetime.date, exp: int):
    # WHEN
    d = tfromdate(given)
    # EXPECT
    assert d == exp


@pytest.mark.parametrize(
    ("given", "exp"),
    [
        (("123", "this is my desc"), "123_this_is_my_desc"),
        ((123, "this is my desc"), "123_this_is_my_desc"),
        (("1", "thisismydesc"), "1_thisismydesc"),
        ((1, "thisismydesc"), "1_thisismydesc"),
        (("456", ""), "456"),
        ((456, ""), "456"),
        (("111", "this_is my_desc"), "111_this_is_my_desc"),
        ((111, "this_is my_desc"), "111_this_is_my_desc"),
    ],
)
def test_merge_id_desc(given: Tuple[Union[int, str], str], exp: str):
    # WHEN
    res = merge_id_desc(*given)
    unstyled = click.unstyle(res)
    # EXPECT
    assert str(given[0]) in res
    assert unstyled == exp


@pytest.mark.parametrize(
    ("given", "exp"),
    [
        ("123_this_is_my_desc", ("123", "this is my desc")),
        ("1_thisismydesc", ("1", "thisismydesc")),
        ("456", ("456", None)),
        ("111_this_is_my_desc", ("111", "this is my desc")),
    ],
)
def test_unmerge_id_desc(given: str, exp: Tuple[Union[int, str], str]):
    # WHEN
    res = unmerge_id_desc(given)
    # EXPECT
    assert res == exp


@pytest.mark.parametrize(
    ("given", "exp"),
    [
        ("  03:30 ", (3, 30)),
        ("3:30  ", (3, 30)),
        ("  03:0", (3, 0)),
        ("3:0", (3, 0)),
        ("03:00", (3, 0)),
        ("3.00", (3, 0)),
        (" 3.5  ", (3, 30)),
        (" 3.5", (3, 30)),
    ],
)
def test_parse_ore_minuti(given: str, exp: Tuple[int, int]):
    # WHEN
    res = parse_ore_minuti(given)
    # EXPECT
    assert res == exp

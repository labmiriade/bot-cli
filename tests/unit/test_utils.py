from typing import Tuple

import pytest

from src.utils import parse_ore_minuti


@pytest.mark.parametrize(('s', 'exp'), [
    ('  03:30 ', (3, 30)),
    ('3:30  ', (3, 30)),
    ('  03:0', (3, 0)),
    ('3:0', (3, 0)),
    ('03:00', (3, 0)),
    ('3.00', (3, 0)),
    (' 3.5  ', (3, 30)),
    (' 3.5', (3, 30)),
])
def test_parse_ore_minuti(s: str, exp: Tuple[int, int]):
    # GIVEN s
    # WHEN
    res = parse_ore_minuti(s)
    # EXPECT
    assert res == exp

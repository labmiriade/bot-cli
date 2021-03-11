import os
from typing import Dict, List, Any

import pytest

from src.cli_utils import merge, envvar_to_config_path, load_default_map

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    ("config", "path", "value", "expected"),
    [
        ({}, ["a"], 1, {"a": 1}),
        ({"a": 0}, ["a"], 1, {"a": 1}),
        ({"a": 0}, ["b"], 1, {"a": 0, "b": 1}),
        ({"a": {"b": 0}}, ["a", "c"], "c", {"a": {"b": 0, "c": "c"}}),
        ({"a": {"b": 0}}, ["a", "b"], 2, {"a": {"b": 2}}),
        ({"a": {"b": 0}}, ["c", "d"], 3, {"a": {"b": 0}, "c": {"d": 3}}),
    ],
)
def test_merge(config: Dict, path: List[str], value: Any, expected: Dict):
    # WHEN
    res = merge(config, path, value)
    # EXPECT
    assert res == expected


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("BOT_RAPP_LS_COUNT", ["rapp", "ls", "count"]),
        ("BOT_RAPP_ADD_SEDE", ["rapp", "add", "sede"]),
    ],
)
def test_envvar_to_config_path(given: str, expected: List[str]):
    # WHEN
    res = envvar_to_config_path(given)
    # EXPECT
    assert res == expected


@pytest.mark.parametrize(
    ("location", "envvars", "expected"),
    [
        (os.path.join(THIS_DIR, "sample_config.toml"), {}, {"rapp": {"ls": {"count": 3}}}),
        (os.path.join(THIS_DIR, "sample_config.toml"), {}, {"rapp": {"ls": {"count": 3, "foo": "4"}}}),
        (os.path.join(THIS_DIR, "sample_config.toml"), {}, {"rapp": {"ls": {"count": "foo"}}}),
    ],
)
def test_load_default_map(location: str, envvars: Dict[str, str], expected: Dict):
    config = load_default_map(location, {})
    expected = {
        "rapp": {
            "ls": {
                "count": 3,
            }
        }
    }
    assert config == expected

from typing import Dict, List, Any

import pytest

from src.cli_utils import merge, envvar_to_config_path, load_default_map


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
        ("BOT_RAPP_LS_COUNT", ["bot", "rapp", "ls", "count"]),
        ("BOT_RAPP_ADD_SEDE", ["bot", "rapp", "add", "sede"]),
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
        ("./sample_config", {}, {"rapp": {"ls": {"count": 3}}}),
        ("./sample_config", {}, {"rapp": {"ls": {"count": 3, "foo": "4"}}}),
        ("./sample_config", {}, {"rapp": {"ls": {"count": "foo"}}}),
    ],
)
def test_load_default_map(location: str, envvars: Dict[str, str], expected: Dict):
    location = "./sample_config.toml"
    config = load_default_map(location, {})
    expected = {
        "rapp": {
            "ls": {
                "count": 3,
            }
        }
    }
    assert config == expected

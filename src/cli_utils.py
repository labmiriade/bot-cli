"""
Questo file contiene alcuni metodi utili per la gestione degli
argomenti da linea di comando.

Ad esempio per trovare gli argomenti di default.
"""
import copy
import os
from pathlib import Path
from typing import Tuple, Dict, List, Any, Optional

import toml

CONFIG_FILE = os.path.join(Path.home(), ".mirbot")
ENV_VAR_PREFIX = "BOT_"
CONFIG_COMMENT = """# Questo file contiene le configurazioni dei default della CLI di BOT
#
# Puoi mettere un valore di default per tutti i comandi
# basta che il file sia un file toml ben formattato
# e i nomi delle chiavi siano gli stessi dei sottocomandi e delle opzioni.
# Ad esempio per impostare il default:
#    bot rapp ls --count 3
# Devi compilare il file toml con:
#    [rapp]
#    [rapp.ls]
#    count = 3
#
# Quando c'è un valore di default quello viene utilizzato saltando eventuali
# prompt.
# Ad esempio se aggiungo:
#    [rapp]
#    [rapp.add]
#    sede = 2
# Non comparirà il prompt che chiede quale sia la sede selezionata (e verrà
# usato il default).
# Se si vuole che il valore sia solo evidenziato si può utilizzare un "soft"
# default (che si ottiene indicando `~soft` come suffisso dell'opzione).
# Ad esempio se si imposta:
#    [rapp]
#    [rapp.add]
#    "sede~soft" = 2
# la sede "2" verrà pre-selezionata e si potrà premere invio per evidenziarla.

"""


def stored_creds(location: str = CONFIG_FILE) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns the credentials looking for env vars and in the config file
    """
    creds = get_stored_config(location).get("creds", {})
    username = os.environ.get("BOT_USERNAME") or creds.get("username")
    password = os.environ.get("BOT_PASSWORD") or creds.get("password")
    return username, password


def envorconfig(env: str, keys: Tuple):
    return
    aux = os.environ.get(env)
    if aux is not None:
        return aux
    c = config
    try:
        for k in keys:
            c = c[k]
        aux = c
    except KeyError:
        aux = None
    return aux


def get_default(path: List[str], location: str = CONFIG_FILE, envvars: Dict[str, str] = os.environ) -> Optional[Any]:
    # look for an env var
    var_name = ENV_VAR_PREFIX + "_".join(path).upper()
    aux = envvars.get(var_name)
    if aux is not None:
        return aux
    # look in config file
    aux = get_stored_config(location)
    for el in path:
        if not isinstance(aux, dict):
            aux = {}
        aux = aux.get(el)
    return aux


def put_stored_config(config: Dict, location: str = CONFIG_FILE):
    """
    Save the configuration to the specified file
    """
    # Override the toml config file
    with open(location, "w") as f:
        f.write(CONFIG_COMMENT)
        toml.dump(config, f)


def get_stored_config(location: str = CONFIG_FILE) -> Dict:
    """
    Read the defaults from a toml file
    """
    # create defaults from config file
    try:
        with open(location, "r") as f:
            config = toml.load(f) or {}
    except FileNotFoundError:
        config = {}
    return config


def load_default_map(location: str = CONFIG_FILE, envvars: Dict[str, str] = os.environ.items()) -> Dict:
    """
    Returns the default map for the CLI
    The default map holds default values for every parameter
    """
    config = get_stored_config(location)

    # override defaults from environment variables
    for key, value in envvars:
        path = envvar_to_config_path(key)
        if value == "":
            # empty string should unset the value
            value = None
        if path is not None:
            # if the path is not none, merge it!
            old = copy.deepcopy(config)
            config = merge(old, path, value)

    return config


def merge(config: Dict, path: List[str], value: Any) -> Any:
    """
    Replaces the value in a dictionary at the specified path
    """
    if len(path) == 0:
        return value
    else:
        key = path[0]
        old = copy.deepcopy(config.get(key))
        if not isinstance(old, dict):
            old = {}
        config[key] = merge(old, path[1:], value)
        return config


def envvar_to_config_path(key: str) -> Optional[List[str]]:
    """
    Given the name of an environment variable returns the path
    in the config object where it should reside if it is a bot value
    Examples:
        - BOT_RAPP_LS_COUNT becomes ['bot', 'rapp', 'ls', 'count']
        - BOT_RAPP_ADD_SEDE becomes ['bot', 'rapp', 'add', 'sede']
        - JAVA_HOME becomes None
    """
    if not key.startswith(ENV_VAR_PREFIX):
        # the env var is not for bot-cli
        return None
    path = key.lower().split("_")
    if len(path) < 2:
        # the path is too short as the first item is always
        # `bot` with the given PREFIX
        return None
    return path[1:]

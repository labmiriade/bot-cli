"""
Questo file contiene alcuni metodi utili per la gestione degli
argomenti da linea di comando.

Ad esempio per trovare gli argomenti di default.
"""
import os
from pathlib import Path
from typing import Tuple

import click
import toml

from src import USERNAME_ENV_VAR, PASSWORD_ENV_VAR

CONFIG_FILE = os.path.join(Path.home(), ".mirbot")

try:
    with open(CONFIG_FILE, "r") as f:
        config = toml.load(f) or {}
except FileNotFoundError:
    config = {}


def envorconfig(env: str, keys: Tuple):
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


class CredsCommand(click.core.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username_help = f"""
        Usa il file di configurazione (bot config) oppure la variabile
        d'ambiente {USERNAME_ENV_VAR} per impostare il tuo username
        (che coincide con l'email aziendale).
        """
        username_help = "the username to use"
        password_help = f"""
        Usa il file di configurazione (bot config) oppure la variabile
        d'ambiente {PASSWORD_ENV_VAR} per impostare la tua password
        (se non sai quale sia clicca su "ho dimenticato la password"
        nella homepage di bot).
        """
        password_help = "the password to use"
        opt_0 = click.core.Option(
            ("--username",),
            default=envorconfig(USERNAME_ENV_VAR, ("creds", "username")),
            required=True,
            help=username_help,
        )
        opt_1 = click.core.Option(
            ("--password",),
            default=envorconfig(PASSWORD_ENV_VAR, ("creds", "password")),
            required=True,
            help=password_help,
        )
        self.params.insert(0, opt_0)
        self.params.insert(1, opt_1)


class AliasedGroup(click.Group):
    """
    A class for a group able to match subcommands even if only a substring is matched

    Examples:
        bot wh -> bot whoami (because there is no other command starting with `wh`)
    """

    def get_command(self, ctx, cmd_name):
        """
        Override get_command to return commands if matching a unique substring (es. rapp for rapportini)
        Args:
            ctx ():
            cmd_name ():

        Returns:
            the command that matched if it is unique, a fail if it is not unique, None if no command matches
        """
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return super().get_command(ctx, matches[0])
        else:
            ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))

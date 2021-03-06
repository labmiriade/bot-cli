from shutil import rmtree

import click

from ..repositories.bot import CACHE_DIR


@click.command(help="Rimuove la cache")
def svuota_cache():
    """
    Flush the cache
    """
    rmtree(CACHE_DIR)
    click.secho(" 🐷 Eliminata tutta la cache! 🗑", fg="magenta")

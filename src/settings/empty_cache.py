from shutil import rmtree

import click

from src.repo import CACHE_DIR


@click.command(help="Rimuove la cache")
def svuota_cache():
    """
    Flush the cache
    """
    rmtree(CACHE_DIR)
    click.secho(f" 🐷 Eliminata tutta la cache! 🗑", fg="magenta")

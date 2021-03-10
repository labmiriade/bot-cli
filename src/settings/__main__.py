import click

from .autocompletion import auto_completamento
from .empty_cache import svuota_cache
from .whoami import whoami


@click.group(help="Impostazioni della cli")
def settings():
    """
    The group for holding commands on rapportini
    """
    pass


settings.add_command(auto_completamento)
settings.add_command(svuota_cache)
settings.add_command(whoami)

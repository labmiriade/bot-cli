import os
from shutil import rmtree

import click

from src.repo import CACHE_DIR


@click.group(help="Impostazioni della cli")
def settings():
    """
    The group for holding commands on rapportini
    """
    pass


@settings.command(help="Rimuove la cache")
def svuota_cache():
    """
    Flush the cache
    """
    rmtree(CACHE_DIR)
    click.secho(f" 🐷 Eliminata tutta la cache! 🗑", fg="magenta")


@settings.command(help="Abilita autocompletamento")
def completamento():
    """
    Helps configuring autocompletions of commands
    """
    current_shell = os.environ.get("SHELL", "").split("/")[-1]
    if current_shell != "":
        current_shell = f' (al momento sembra che tu stia usando "{current_shell}")'
    fst = (
        "\n 🐷 Puoi abilitare l'autocompletamento per aiutarti con i comandi\n"
        "    e soprattutto con le commesse e i task quando inserisci i rapportini.\n"
    )
    snd = "  Per l'autocompletamento controlla qual è la shell che usi\n" "  e copia il comando nel file indicato.\n"

    def print_instructions(shell: str, file: str, command: str):
        content = f"  Se usi {click.style(shell, fg='bright_magenta')} aggiungi a '{file}'\n" f"     {command}\n"
        click.echo(content)

    instructions = [
        ("bash", "~/.bashrc", 'eval "$(_BOT_COMPLETE=source_bash bot)"'),
        ("zsh", "~/.zshrc", 'eval "$(_BOT_COMPLETE=source_zsh bot)"'),
        ("fish", "~/.config/fish/completions/bot.fish", "eval (env _BOT_COMPLETE=source_fish bot)"),
    ]

    lst = f" 🐷 Se hai problemi a far funzionare l'autocompletamento fammi sapere!"

    click.secho(fst, fg="magenta")
    click.secho(snd)
    for i in instructions:
        print_instructions(*i)
        click.echo()
    click.secho(lst, fg="magenta")

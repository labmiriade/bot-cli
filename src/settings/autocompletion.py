import os

import click


@click.command(help="Abilita autocompletamento")
def auto_completamento():
    """
    Helps configuring autocompletions of commands
    """
    current_shell = os.environ.get("SHELL", "").split("/")[-1]
    current_shell_detected = (
        f' (al momento sembra che tu stia usando "{current_shell}")' if current_shell is not None else ""
    )
    fst = (
        "\n 🐷 Puoi abilitare l'autocompletamento per aiutarti con i comandi\n"
        "    e soprattutto con le commesse e i task quando inserisci i rapportini.\n"
    )
    snd = (
        f"  Per l'autocompletamento controlla quale shell usi{current_shell_detected}\n"
        f"  e copia il comando nel file indicato.\n"
    )

    def print_instructions(shell: str, file: str, command: str):
        highlights = "blue" if shell == current_shell else None
        ind = " " * 2
        ttl = f"{ind}Se usi {click.style(shell, fg='bright_magenta')} aggiungi a '{click.style(file, fg=highlights)}'"
        cmd = f"{ind}   {click.style(command, fg=highlights)}"
        click.echo(ttl)
        click.echo(cmd)

    instructions = [
        ("bash", "~/.bashrc", 'eval "$(_BOT_COMPLETE=source_bash bot)"'),
        ("zsh", "~/.zshrc", 'eval "$(_BOT_COMPLETE=source_zsh bot)"'),
        ("fish", "~/.config/fish/completions/bot.fish", "eval (env _BOT_COMPLETE=source_fish bot)"),
    ]

    lst = " 🐷 Se hai problemi a far funzionare l'autocompletamento fammi sapere!"

    click.secho(fst, fg="magenta")
    click.secho(snd)
    for i in instructions:
        print_instructions(*i)
        click.echo()
    click.secho(lst, fg="magenta")

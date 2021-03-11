import click

from src.cli_utils import get_stored_config, put_stored_config
from src.rapportini.rapportini_printer import offices_choices


@click.command(help="Configura BOT nel terminale")
def config():
    """
    Allows the user to update the saved configurations in the .mirbot toml file
    """
    # read the current values, to present them as defaults
    current_values = get_stored_config()
    click.secho(" 🐷 Ora ti guiderò nell'impostazione delle configurazioni principali\n", fg="magenta")

    # Credentials
    #  update username and password
    creds = current_values.get("creds", {})
    click.secho("Inserisci la tua mail aziendale", fg="green")
    creds["username"] = click.prompt("  username", default=creds.get("username"), type=click.STRING)
    click.echo("")  # add a newline char
    click.secho("Inserisci la tua password, se non la conosci perché entri", fg="cyan")
    click.secho('sempre con Google clicca su "password dimenticata" in homepage', fg="cyan")
    creds["password"] = click.prompt("  password", default=creds.get("password"), hide_input=True, type=click.STRING)
    click.echo("")  # add a newline char
    # if the user enters a space, remove the associated value in config
    if creds["username"].strip() == "":
        creds["username"] = None
    if creds["password"].strip() == "":
        creds["password"] = None
    current_values["creds"] = creds

    # Rapp
    #  default office
    rapp = current_values.get("rapp", {})
    add = rapp.get("add", {})
    click.secho(
        "Impostiamo ora l'ufficio di default per i nuovi rapportini\n(potrai comunque cambiarlo ogni volta)",
        fg="bright_magenta",
    )
    click.secho("Le sedi sono:", fg="bright_magenta")
    for office in offices_choices:
        click.secho(f"  - {office}", fg="bright_magenta")
    click.secho("Basta indicare il numero della relativa sede", fg="bright_magenta")
    add["sede~soft"] = click.prompt("  sede", default=add.get("sede~soft"), type=click.STRING)
    if add["sede~soft"].strip() == "":
        add["sede~soft"] = None
    rapp["add"] = add
    current_values["rapp"] = rapp
    click.echo("")  # add a newline char

    put_stored_config(current_values)

    click.secho(" 🐷 Finito! se vuoi modificare il file manualmente, lo trovi in ~/.mirbot", fg="magenta")

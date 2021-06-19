import copy
import datetime
from typing import Optional

import click

from .rapportini_printer import offices_choices, full_rapp
from ..cli_utils import stored_creds, get_default
from ..repositories import location_finder
from ..repositories.bot import Bot, Commessa, Rapportino
from ..utils import merge_id_desc, unmerge_id_desc, parse_ore_minuti


def _create_bot() -> Optional[Bot]:
    """
    Workaround because reading ctx.obj in autocomplete methods
    seems not working.

    See Also:
        - https://github.com/pallets/click/pull/1679
    """
    username, password = stored_creds()
    if username is None or password is None:
        return None
    return Bot(username, password)


def get_commesse_compl(ctx, args, incomplete: str):
    """
    Allows for autocompletion of the commesse
    Args:
        ctx (): the context of the command
        args (Iterable[str]): an Iterable of arguments for the current item
        incomplete (): a string with the characters typed until now (can be an empty string)

    Returns:
        a list of autocompletion strings
    """
    # noinspection PyStatementEffect
    try:
        bot = ctx.obj or _create_bot()  # take the bot from the ctx or init a new one
        commesse = bot.commesse
        commesse_compl = map(lambda c: merge_id_desc(c["jobId"], c["description"]), commesse)
        i = incomplete.lower()
        return [c for c in commesse_compl if i in c.lower()]
    except:  # noqa: E722 bare exeption in autocomplete are allowed
        return []


def get_attivita_compl(ctx, args, incomplete: str):
    """
    Allows for autocompletion of the attività reading the commessa
    Args:
        ctx (): the context of the command
        args (Iterable[str]): an Iterable of arguments for the current item (the last one is the commessa)
        incomplete (): a string with the characters typed until now (can be an empty string)

    Returns:
        a list of autocompletion strings
    """
    # noinspection PyBroadException
    try:
        bot = ctx.obj or _create_bot()
        job_id = unmerge_id_desc(args[-1])[0]
        activities = bot.activities(job_id)
        i = incomplete.lower()
        return [
            merge_id_desc(a["taskId"], a["description"])
            for a in activities
            if i in a["description"].lower() or i in a["taskId"].lower()
        ]
    except:  # noqa: E722 bare exeption in autocomplete are allowed
        return []


def validate_office(ctx, params, value):
    """
    This is a callback to verify that the inserted office exists and is a valid one
    Args:
        ctx (): the context of the command
        params (): the params to this validator
        value (): the value inputed by the user

    Returns:
        the office if it is valid (with complete value)
    Raises:
        (click.BadParameter) if the inputed value is not right
    """
    if value is None:
        return None
    for office in offices_choices:
        if office.lower().startswith(click.unstyle(value).lower()):
            return office
    click.secho(f"{value} is not an accepted value", fg="red")
    raise click.BadParameter("indica il numero della sede")


def office_prompt(default_office: Optional[str]) -> str:
    """
    Returns the prompt for asking the chosen office highlighting the default one
    """
    if default_office is not None:
        matching_offices_idxs = [
            i for i, o in enumerate(offices_choices) if o.lower().startswith(default_office.lower())
        ]
        if len(matching_offices_idxs) == 1:
            default_idx = matching_offices_idxs[0]
        else:
            default_idx = None
    else:
        default_idx = None
    oc = copy.copy(offices_choices)
    if default_idx is not None:
        oc[default_idx] = click.style(oc[default_idx], fg="cyan")
    return f'{click.style("Sede", fg="cyan")} ({", ".join(oc)})'


def validate_date(ctx, args, value) -> datetime.datetime:
    """
    Returns the validated date (if any) and raise a click.BadParameter Exception
    otherwise
    Args:
        ctx ():
        args ():
        value (str): the inputed value for the string

    Returns:
        the validated date as %Y-%m-%d str
    Raises:
        (click.BadParameter): if there the input is not valid
    """
    if isinstance(value, datetime.datetime):
        return value
    date = None
    fmts = ["%Y-%m-%d", "%d-%m-%Y", "%d-%m"]
    # try parsing date
    for fmt in fmts:
        try:
            date = datetime.datetime.strptime(value, fmt)
            break
        except ValueError:
            pass
    # check for keywords
    if value.lower() in ["oggi", "today"]:
        date = datetime.datetime.now()
    elif value.lower() in ["ieri", "yesterday"]:
        date = datetime.datetime.now() - datetime.timedelta(days=1)

    if date is None:
        allowed_formats = ", ".join([f"'{f}'" for f in fmts])
        raise click.BadParameter(f"Inserisci la data in uno dei formati: {allowed_formats}")

    date = date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
    if date.year < 2000:
        date = date.replace(year=datetime.datetime.now().year)
    return date


def _today() -> datetime.datetime:
    """
    Returns today's datetime
    """
    return datetime.datetime.now()


def _yesterday() -> datetime.datetime:
    """
    Returns yesterday's datetime
    """
    return datetime.datetime.now() - datetime.timedelta(days=1)


@click.command(help="Aggiungi un nuovo rapportino")
# the first argument is the commessa
@click.argument("commessa", type=click.STRING, autocompletion=get_commesse_compl)
# the second argument is the activity for the given commessa
@click.argument("attivita", type=click.STRING, autocompletion=get_attivita_compl)
# the date in which the rapportino should be inserted
@click.option("--oggi", "data", type=click.STRING, flag_value=_today())
@click.option("--ieri", "data", type=click.STRING, flag_value=_yesterday())
@click.option(
    "-d",
    "--data",
    type=click.STRING,
    default=lambda: _today().strftime("%d-%m-%Y"),
    prompt=click.style("Data", fg="green"),
    help='La data per cui va inserito il rapportino in formato ("%Y-%m-%d", "%d-%m-%Y" o "%d-%m")',
    callback=validate_date,
    show_default="oggi",
)
# the amount of ore to add to the rapportino
@click.option(
    "-o",
    "--ore",
    type=click.STRING,
    prompt=click.style("Ore", fg="bright_green"),
    default="8:00",
    help="Durata in ore[:minuti]",
)
# the description to put in the rapportino
@click.option(
    "--descrizione",
    type=click.STRING,
    prompt="Descrizione",
    help="La descrizione delle attività svolte, visibile anche al cliente",
)
# the optional internal note to put in the rapportino
@click.option(
    "--note",
    type=click.STRING,
    prompt="Note",
    default="",
    help="Le note interne associate a questa attività, non saranno visibili al cliente",
)
# the office to put in the rapportino
@click.option(
    "-s",
    "--sede",
    type=click.STRING,
    default=None,
    callback=validate_office,
    help="Indica la sede in cui hai svolto l'attività",
)
# whether the flag trasferta should be inserted
@click.option("--trasferta/--no-trasferta", default=False, help="l'attività è stata svolta in trasferta")
# whether the flag fatturare should be inserted
@click.option("--fatturare/--no-fatturare", default=None, help="l'attività va fatturata")
# whether the flag prepagata should be inserted
@click.option("--prepagata/--no-prepagata", default=None, help="l'attività è prepagata")
# whether the flag straordinaio should be inserted
@click.option("--straordinario/--no-straordinario", default=False, help="è uno straordinario")
@click.pass_context
def add(
    ctx,
    commessa,
    attivita,
    data: datetime.datetime,
    ore,
    sede,
    descrizione,
    note,
    trasferta,
    fatturare,
    prepagata,
    straordinario,
):
    # parse inputed time
    ore, minuti = parse_ore_minuti(ore)
    # sanitize inputed date setting timezone and getting the right timestamp
    if isinstance(data, str):
        data = validate_date(object, [], data)
    data = data.replace(tzinfo=datetime.timezone.utc)
    if data.year < 2000:
        data = data.replace(year=datetime.datetime.now().year)
    date = int(data.timestamp()) * 1000

    # get the the job description from the job_id
    job_id = unmerge_id_desc(commessa)[0]
    full_commessa: Commessa = ctx.obj.get_commessa(job_id)

    # set the location
    if sede is None:
        today = datetime.date.today()
        predicted_office: Optional[str] = None  # try to predict the user's location

        # check if the date is today and the user is in some location
        if data.year == today.year and data.month == today.month and data.day == today.day:
            predicted_office = location_finder.current_location()

        # if the location is predicted, use it
        # otherwise rely on user config
        if predicted_office is not None:
            office = predicted_office
            office_name = " ".join(predicted_office.split("_")[1:])
            click.secho(
                f"in base alla data dei rapportini e alla tua posizione, deduco tu sia a {office_name}",
                fg="bright_black",
            )
        else:
            office = get_default(["rapp", "add", "sede~soft"])

        sede = click.prompt(office_prompt(office), value_proc=validate_office, default=office)

    # get office_id from sede
    office_id = unmerge_id_desc(sede)[0]

    # create the Rapportino to store default and inputed data
    r = Rapportino(
        rapportinoId=-1,
        commessa=full_commessa["description"],
        jobId=int(job_id),
        attivita=attivita,
        jobTaskId=int(unmerge_id_desc(attivita)[0]),
        date=date,
        note=note,
        tecnicoId=int(ctx.obj.res_id),
        customerId=int(full_commessa["customerId"]),
        customerName=full_commessa["customerId"],
        description=descrizione,
        quantityHours=ore,
        quantityMinutes=minuti,
        officeId=office_id,
        flagTransfert=trasferta,
        flagPay=fatturare if fatturare is not None else full_commessa["toBePay"],
        flagPrepay=prepagata if prepagata is not None else full_commessa["flagPrepayed"],
        flagExtraHour=straordinario,
    )
    try:
        # salva il rapportino
        # click.confirm(click.style(" 🐷 Va bene?", fg='magenta'), default=True, abort=True)
        confirmed = False
        printer = full_rapp(indents=1, hide_date=False)
        while not confirmed:
            click.echo("", nl=True)  # newline
            printer(r)  # print the Rapportino
            click.echo("", nl=True)  # newline
            click.secho(" 🐷 Va bene? (f per modificare flag) [y/n/f]: ", fg="magenta", nl=False)
            value = click.getchar(echo=True)
            click.echo("")
            # check if the input is in the
            while value.lower() not in ["y", "n", "f", "\n", "\r", "000A", "000D", "000D000A"]:
                click.secho(f" Non ho capito '{repr(value)}/{[ord(c) for c in value]}', va bene? [y/n/f]", fg="magenta")
                value = click.getchar(echo=True)
                click.echo("")

            if value.lower() in ["n"]:
                raise click.Abort()
            elif value.lower() in ["f"]:
                r["flagTransfert"] = click.confirm("   Trasferta 🚗", default=r["flagTransfert"], abort=False)
                r["flagPrepay"] = click.confirm("   Prepagata 💳", default=r["flagPrepay"], abort=False)
                r["flagPay"] = click.confirm("   Fatturare 💶", default=r["flagPay"], abort=False)
                r["flagExtraHour"] = click.confirm("   Straordinario ⏱", default=r["flagExtraHour"], abort=False)
            elif value.lower() in ["y", "\n"]:
                confirmed = True

        ctx.obj.add_rapportino(
            job_id=r["jobId"],
            task_id=r["jobTaskId"],
            hours=r["quantityHours"],
            minutes=r["quantityMinutes"],
            descrizione=r["description"],
            note=r["note"],
            date=r["date"],
            office_id=r["officeId"],
            flag_transfert=r["flagTransfert"],
            flag_pay=r["flagPay"],
            flag_prepay=r["flagPrepay"],
            flag_extrahour=r["flagExtraHour"],
        )
        # stampa il risultato
        click.secho(" 🐷 Salvato il rapportino! 💪", fg="magenta")
    except click.Abort:
        click.secho(" 🐷 Ok, non procedo!", fg="magenta")
    except Exception as error:
        click.secho(f" 🐷 Errore: {error=}", fg="bright_red")
        exit(1)

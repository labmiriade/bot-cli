import datetime
import os.path
from functools import wraps
from typing import List, Any, Callable, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
from src.cli_utils import MIRBOT_FOLDER

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

TOKEN_LOCATION = os.path.join(MIRBOT_FOLDER, "google-token.json")
CREDENTIALS_LOCATION = "credentials.json"


def _load_credentials(token_location: str = TOKEN_LOCATION) -> Optional[Credentials]:
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_location):
        creds = Credentials.from_authorized_user_file(token_location, SCOPES)
    else:
        creds = None
    # eventually refresh token
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save the credentials for the next run
        with open(token_location, "w") as token:
            token.write(creds.to_json())
    # returns the credentials
    return creds


def authorize_google(
    authorization_prompt_message: str,
    authorization_code_message: str,
    token_location: str = TOKEN_LOCATION,
    credentials_location: str = CREDENTIALS_LOCATION,
):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_location, SCOPES)
    creds = flow.run_console(
        authorization_prompt_message=authorization_prompt_message,
        authorization_code_message=authorization_code_message,
    )
    # Save the credentials for the next run
    with open(token_location, "w") as token:
        token.write(creds.to_json())


def inject_credentials_if_any(f: Callable) -> Callable:
    """
    Returns a `partial` object with the creds injected or None if
    creds are not available.
    """

    @wraps(f)
    def _wrapper(*args: Any, **kwargs: Any):
        creds = _load_credentials()
        if creds is None:
            return None
        return f(*args, creds=creds, **kwargs)

    return _wrapper


def has_google_credentials(token_location: str = TOKEN_LOCATION) -> bool:
    return os.path.exists(token_location)


@inject_credentials_if_any
def get_events_on(date: datetime.date, creds: Credentials) -> List[Any]:
    service = build("calendar", "v3", credentials=creds)
    start = datetime.datetime(date.year, date.month, date.day, tzinfo=datetime.timezone.utc)
    end = start + datetime.timedelta(days=1)
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    return events


if __name__ == "__main__":
    # authorize_google()
    aux = get_events_on(datetime.date(2021, 3, 5))
    print(f"{aux=}")

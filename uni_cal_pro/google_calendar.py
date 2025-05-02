from datetime import timedelta
from googleapiclient import discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from uni_cal_pro import config


SCOPES = ["https://www.googleapis.com/auth/calendar"] # If modifying these scopes, delete the file token.json in the config directory.
CALENDAR_ID_FILENAME = "google_calendar_id.txt"


calendar_id_filepath = os.path.join(config.TEMP_DIRECTORY_PATH, CALENDAR_ID_FILENAME)


def get_user_credentials():
  """Get the credentials needed to manipulate a google calendar from the temp folder."""

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time. It is stored in the OS' default config directory so that sensitive
  # keys are not added to the git.

  API_TOKEN_FILENAME = "token.json"
  API_SECRET_FILENAME = "credentials.json"

  creds = None

  user_signed_in_token_json_path = os.path.join(config.TEMP_DIRECTORY_PATH, API_TOKEN_FILENAME)
  if os.path.exists(user_signed_in_token_json_path):
    creds = Credentials.from_authorized_user_file(user_signed_in_token_json_path, SCOPES)

  # If there are no (valid) credentials available then get new credentials.
  if not creds or not creds.valid:
    # If the only credentials available are expired then refresh them.
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    # Begin the google sign in flow using the api secret file credentials.json.
    else:
      credentials_path = os.path.join(config.TEMP_DIRECTORY_PATH, API_SECRET_FILENAME)

      try:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
      except FileNotFoundError:
        raise FileNotFoundError(f"Please ensure that the api secret file {API_SECRET_FILENAME} is in {config.TEMP_DIRECTORY_PATH}.")
    
    # Save the credentials for the next run.
    with open(user_signed_in_token_json_path, "w") as token:
      token.write(creds.to_json())
  
  return creds

# NOTE this will crash if the credentials.json file does not exist in the temp directory.
def build_service():
  creds = get_user_credentials()
  service = discovery.build("calendar", "v3", credentials=creds)
  return service

def calendar_id_exists(service, calendar_id):
  try:
      service.calendars().get(calendarId=calendar_id).execute()
      return True
  except:
      return False

def save_calendar_id(id):
  with open(calendar_id_filepath, "w") as file:
    file.write(id)

  print("\tCalendar id saved for later use.")

def is_calendar_id_saved():
  return os.path.exists(calendar_id_filepath)

def get_saved_calendar_id():
  if is_calendar_id_saved:
      with open(calendar_id_filepath) as file:
          return file.read()
  else:
      raise FileNotFoundError(f"The file {calendar_id_filepath} does not exist.")



def add_events(service, calendar_id, events):
  """Add a list of events to Google Calendar. Do not overwrite/duplicate events existing in the same calendar at the same time."""

  def event_exists(service, calendar_id, event):
    events_result = service.events().list(
        calendarId=calendar_id,
        # Add a time delta to these to allow Google Calendar to search within the window.
        timeMin=(event.begin - timedelta(minutes=1)).isoformat(),
        timeMax=(event.end + timedelta(minutes=1)).isoformat(),
        # singleEvents ensures that recurring events are treated as individual events, rather than a single master event happening once.
        singleEvents=True,
    ).execute()

    matching_events = [e for e in events_result.get("items", []) if e.get("summary").lower() == event.name.lower()]

    if matching_events:
      return True
    else:
      return False

  def add_event(service, calendar_id, event):
    new_event = {
      "summary": event.name,
      "location": event.location,
      "description": event.description,
      "start": {
        "dateTime": event.begin.isoformat(),
      },
      "end": {
        "dateTime": event.end.isoformat(),
      },
    }
    
    event_summary = new_event["summary"]
    print(f"\tAdding event: {event_summary}")
    service.events().insert(calendarId=calendar_id, body=new_event).execute()


  event_tally = 0

  for event in events:
      # If the event does not already exist then add it.
      if not event_exists(service, calendar_id, event):
          add_event(service, calendar_id, event)
          event_tally += 1
      
  print(f"\t{event_tally} events added to Google Calendar.")
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def get_calendar_service():
    """Gets or establishes the Google Calendar API service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                print("credentials.json not found. Please follow the instructions to set up Google API credentials.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def create_calendar_event(doctor_email, patient_email, doctor_name, patient_name, date, start_time, end_time):
    """Creates a calendar event for a booked appointment."""
    try:
        service = get_calendar_service()
        if not service:
            print("Google Calendar service could not be initialized.")
            return False

        # Combine date and time (assuming naive local time)
        start_datetime = datetime.datetime.combine(date, start_time)
        end_datetime = datetime.datetime.combine(date, end_time)
        
        # We assume local timezone is relevant for the users of this system
        # If the system expands across timezones, we would use pytz to localize.
        # Format for Google API: "2015-05-28T09:00:00-07:00"
        # We append Z (UTC) or local offset dynamically, for this local system we can let Google infer from a naive isoformat if timeZone parameter is supplied.
        
        event = {
          'summary': f'Appointment with Dr. {doctor_name}',
          'description': f'Patient: {patient_name}',
          'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata', # Defaulting to IST based on prompt hints, adjust if needed!
          },
          'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
          },
          'attendees': [
            {'email': doctor_email},
            {'email': patient_email}, # sendUpdates='all' sends invitations automatically
          ],
        }

        event_result = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
        print(f"Event created: {event_result.get('htmlLink')}")
        return True

    except Exception as e:
        print(f"Error creating calendar event: {str(e)}")
        # If calendar fails, we catch it here so the booking still succeeds normally
        return False

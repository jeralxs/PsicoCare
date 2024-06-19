from __future__ import print_function
import os.path
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.apps import meet_v2


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/meet']

# 'https://www.googleapis.com/auth/meetings.space.created',
# SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/meet']
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    # "https://www.googleapis.com/auth/meetings.space.created",
    # "https://www.googleapis.com/auth/meet",
]

# class GoogleWorkspaceManager:
#     def __init__(self):
#         self.creds = self._authenticate()
#         self.calendar_service = build("calendar", "v3", credentials=self.creds)
#         self.meet_service = meet_v2.SpacesServiceAsyncClient(credentials=self.creds)

#     def _authenticate(self):
#         creds = None
#         if os.path.exists("token.json"):
#             creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
def crear_credenciales():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    # Realiza el flujo de autorización
    creds = flow.run_local_server(port=0)

    # Guarda las credenciales en un archivo
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    return creds

def obtener_credenciales():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Verifica si las credenciales son válidas y refresca si es necesario
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = crear_credenciales()

        # Guarda las credenciales actualizadas
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
def GoogleMeetManager():
    """Shows basic usage of the Google Meet API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

    # try:
    #     client = meet_v2.SpacesServiceClient(credentials=creds)
    #     request = meet_v2.CreateSpaceRequest()
    #     response = client.create_space(request=request)
    #     print(f'Space created: {response.meeting_uri}')
    # except Exception as error:
    #     # TODO(developer) - Handle errors from Meet API.
    #     print(f'An error occurred: {error}')


if __name__ == '__main__':
    GoogleMeetManager()

async def create_space():
    # Create a client
    client = meet_v2.SpacesServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.CreateSpaceRequest(
    )

    # Make the request
    response = await client.create_space(request=request)

    # Handle the response
    print(response.meeting_uri)


async def get_space():
    # Create a client
    client = meet_v2.SpacesServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.GetSpaceRequest(
        name="name_value",
    )

    # Make the request
    response = await client.get_space(request=request)

    # Handle the response
    print(response)

async def update_space():
    # Create a client
    client = meet_v2.SpacesServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.UpdateSpaceRequest(
    )

    # Make the request
    response = await client.update_space(request=request)

    # Handle the response
    print(response)

async def end_active_conference():
    # Create a client
    client = meet_v2.SpacesServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.EndActiveConferenceRequest(
        name="name_value",
    )

    # Make the request
    await client.end_active_conference(request=request)


async def list_conference_records():
    # Create a client
    client = meet_v2.ConferenceRecordsServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.ListConferenceRecordsRequest(
    )

    # Make the request
    page_result = client.list_conference_records(request=request)

    # Handle the response
    async for response in page_result:
        print(response)

async def get_conference_record():
    # Create a client
    client = meet_v2.ConferenceRecordsServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.GetConferenceRecordRequest(
        name="name_value",
    )

    # Make the request
    response = await client.get_conference_record(request=request)

    # Handle the response
    print(response)

async def list_participants():
    # Create a client
    client = meet_v2.ConferenceRecordsServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.ListParticipantsRequest(
        parent="parent_value",
    )

    # Make the request
    page_result = client.list_participants(request=request)

    # Handle the response
    async for response in page_result:
        print(response)

async def get_participant():
    # Create a client
    client = meet_v2.ConferenceRecordsServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.GetParticipantRequest(
        name="name_value",
    )

    # Make the request
    response = await client.get_participant(request=request)

    # Handle the response
    print(response)


async def list_participant_sessions():
    # Create a client
    client = meet_v2.ConferenceRecordsServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.ListParticipantSessionsRequest(
        parent="parent_value",
    )

    # Make the request
    page_result = client.list_participant_sessions(request=request)

    # Handle the response
    async for response in page_result:
        print(response)


async def get_participant_session():
    # Create a client
    client = meet_v2.ConferenceRecordsServiceAsyncClient()

    # Initialize request argument(s)
    request = meet_v2.GetParticipantSessionRequest(
        name="name_value",
    )

    # Make the request
    response = await client.get_participant_session(request=request)

    # Handle the response
    print(response)


class GoogleCalendarManager:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)

    def list_upcoming_events(self, max_results=10):
        now = dt.datetime.utcnow().isoformat() + "Z"
        tomorrow = (dt.datetime.now() + dt.timedelta(days=5)).replace(hour=23, minute=59, second=0, microsecond=0).isoformat() + "Z"

        events_result = self.service.events().list(
            calendarId='primary', timeMin=now, timeMax=tomorrow,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'],event['id'])
        
        return events

    def create_event(self, summary, start_time, end_time, timezone, attendees=None):
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            }
        }

        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        try:
            event = self.service.events().insert(calendarId="primary", body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
        except HttpError as error:
            print(f"An error has occurred: {error}")

    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
        if summary:
            event['summary'] = summary

        if start_time:
            event['start']['dateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')

        if end_time:
            event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        updated_event = self.service.events().update(
            calendarId='primary', eventId=event_id, body=event).execute()
        return updated_event
    
    def get_event_details(self, event_id):
        try:
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            return event
        except HttpError as error:
            print(f"An error has occurred: {error}")

    def delete_event(self, event_id):
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            print("Event deleted successfully.")
        except HttpError as error:
            print(f"An error occurred while deleting the event: {error}")

     
    

calendar = GoogleCalendarManager()

calendar.list_upcoming_events()

#calendar.create_event("Hola mundo", "2024-05-06T16:30:00-04:00", "2024-05-06T17:30:00-04:00", "America/Santiago", ["psicocareduoc@gmail.com"])

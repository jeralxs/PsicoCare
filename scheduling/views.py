from __future__ import print_function
from django.shortcuts import render

# Create your views here.

import os.path
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.apps import meet_v2
import pickle



# Ruta al archivo de credenciales
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'
SCOPES = ['https://www.googleapis.com/auth/calendar']

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


def list_events(request):
    service = GoogleCalendarManager()
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return render(request, 'scheduling/events.html', {'events': events})


from django.shortcuts import render, redirect
from .models import Schedule, Appointment
from django.contrib.auth.decorators import login_required
from core.models import Psicologo, Usuario, Paciente, Pacientepsicologo



@login_required
def create_schedule(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time') 
        usuario = Usuario.objects.get(user=request.user)
        psico = Psicologo.objects.get(psi_idusuario=usuario)
        try:
            Schedule.objects.create(psicologo=psico, start_time=start_time, end_time=end_time)
            return redirect('list_schedule')
        except Exception as error:
            print(f'An error occurred: {error}')
    return render(request, 'scheduling/create_schedule.html')

@login_required
def list_schedule(request):
    usuario = Usuario.objects.get(user=request.user)
    psico = Psicologo.objects.get(psi_idusuario=usuario)
    schedules = Schedule.objects.filter(psicologo=psico.idpsicologo)
    return render(request, 'scheduling/list_schedule.html', {'schedules': schedules})

def view_schedule(request,psico_id):
    context = obtener_info_schedule(psico_id)
    return render(request, 'scheduling/view_schedule.html', context)

def obtener_info_schedule(psico_id):

    schedule = Schedule.objects.filter(psicologo=psico_id)
    return {
        'schedules': schedule
    }


@login_required
def book_appointment(request, schedule_id):
    schedule = Schedule.objects.get(schedule_id=schedule_id)
    if request.method == 'POST':
        usuario = Usuario.objects.get(user=request.user)
        paciente = Paciente.objects.get(pac_idusuario=usuario)
        Appointment.objects.create(paciente=paciente, psicologo=schedule.psicologo, schedule=schedule)
        schedule.available = False
        schedule.save()
        Pacientepsicologo.objects.create(psicologo_idusuario=schedule.psicologo, paciente_idusuario=paciente)
        return redirect('list_appointments')
    return render(request, 'scheduling/book_appointment.html', {'schedule': schedule})

@login_required
def list_appointments(request):
    usuario = Usuario.objects.get(user=request.user)
    paciente = Paciente.objects.get(pac_idusuario=usuario)
    appointments = Appointment.objects.filter(paciente=paciente)

    return render(request, 'scheduling/list_appointments.html', {'appointments': appointments})

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






     
    

calendar = GoogleCalendarManager()

calendar.list_upcoming_events()

#calendar.create_event("Hola mundo", "2024-05-06T16:30:00-04:00", "2024-05-06T17:30:00-04:00", "America/Santiago", ["psicocareduoc@gmail.com"])

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
from google_meet.models import Sesion



# Ruta al archivo de credenciales
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'
SCOPES = ['https://www.googleapis.com/auth/calendar']

from django.shortcuts import render, redirect
from .models import Schedule, Appointment
from django.contrib.auth.decorators import login_required
from core.models import Psicologo, Usuario, Paciente, Pacientepsicologo
from google_meet.views import crear_espacio
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from .google_calendar import GoogleCalendarManager, obtener_credenciales
# from googleapiclient.errors import HttpError



@login_required
def create_schedule(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time') 
        valor = request.POST.get('valor') 
        usuario = Usuario.objects.get(user=request.user)
        psico = Psicologo.objects.get(psi_idusuario=usuario)
         # Llama al método para crear el evento
#         calendar = GoogleCalendarManager()
#         calendar.create_event(summary, start_time, end_time, timezone, attendees)
        try:
            Schedule.objects.create(psicologo=psico, start_time=start_time, end_time=end_time, valor=valor)
            return redirect('list_schedule')
        except Exception as error:
            print(f'An error occurred: {error}')
    return render(request, 'scheduling/create_schedule.html')

@login_required
def list_schedule(request):
    usuario = Usuario.objects.get(user=request.user)
    psico = Psicologo.objects.get(psi_idusuario=usuario)
    schedules = Schedule.objects.filter(psicologo=psico.idpsicologo)
    agenda = schedules.first()
    if request.method == "POST":
        meeting_uri= crear_espacio(request)
        if meeting_uri:
            appointed = Appointment.objects.get(psicologo=psico)
            paciente = Paciente.objects.get(idpaciente=appointed.paciente.idpaciente)
            sesion = Sesion.objects.create(
                psicologo=psico,
                paciente=paciente,
                meeting_uri=meeting_uri,
                schedule=agenda
            )
            agenda.link_h = "Y"
            agenda.save()
        
            return render(request, 'google_meet/videollamada.html', {'sesion': sesion})
        else:
            return render(request, 'google_meet/error.html', {'message': 'No se pudo crear la videollamada'})
        #crear sesion (dejar habilitado link uwu)
    #     calendar = GoogleCalendarManager()
#     sesiones = calendar.list_upcoming_events()
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






     
    

# calendar = GoogleCalendarManager()

# calendar.list_upcoming_events()

#calendar.create_event("Hola mundo", "2024-05-06T16:30:00-04:00", "2024-05-06T17:30:00-04:00", "America/Santiago", ["psicocareduoc@gmail.com"])

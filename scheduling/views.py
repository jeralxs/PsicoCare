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
from django.http import HttpResponse
from transbank.error.transbank_error import TransbankError
from payments.webpay_config import transaction



# Ruta al archivo de credenciales
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'
SCOPES = ['https://www.googleapis.com/auth/calendar']

from django.shortcuts import render, redirect
from .models import Schedule, Appointment
from django.contrib.auth.decorators import login_required
from core.models import Psicologo, Usuario, Paciente, Pacientepsicologo
from google_meet.views import crear_espacio
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


# def create_google_calendar_event(start_time, end_time, summary, description, attendee_email):
#     # Esta función asume que ya tienes las credenciales almacenadas
#     creds = None
#     # Aquí deberías cargar las credenciales desde donde las tengas almacenadas
#     # Si no son válidas, deberías refrescarlas o solicitar nuevas

#     service = build('calendar', 'v3', credentials=creds)

#     event = {
#         'summary': summary,
#         'description': description,
#         'start': {
#             'dateTime': start_time.isoformat(),
#             'timeZone': 'America/Santiago',
#         },
#         'end': {
#             'dateTime': end_time.isoformat(),
#             'timeZone': 'America/Santiago',
#         },
#         'attendees': [
#             {'email': attendee_email},
#         ],
#     }

#     event = service.events().insert(calendarId='primary', body=event).execute()
#     return event['id']

# @login_required
# def book_appointment(request, schedule_id):
#     schedule = Schedule.objects.get(schedule_id=schedule_id)
#     if request.method == 'POST':
#         usuario = Usuario.objects.get(user=request.user)
#         paciente = Paciente.objects.get(pac_idusuario=usuario)
#         appointment = Appointment.objects.create(paciente=paciente, psicologo=schedule.psicologo, schedule=schedule)
#         schedule.available = False
#         schedule.save()
#         Pacientepsicologo.objects.create(psicologo_idusuario=schedule.psicologo, paciente_idusuario=paciente)

#         # Crear evento en Google Calendar para el psicólogo
        # calendar = GoogleCalendarManager()
#         psicologo_event_id = calendar.create_event(
#             schedule.start_time,
#             schedule.end_time,
#             f"Cita con {paciente.pac_idusuario.user.first_name} {paciente.pac_idusuario.user.last_name}",
#             "Cita de terapia",
#             schedule.psicologo.psi_usuario.user.email
#         )

#         # Crear evento en Google Calendar para el paciente
#         paciente_event_id = calendar.create_event(
#             schedule.start_time,
#             schedule.end_time,
#             f"Cita con Dr. {schedule.psicologo.psi_usuario.user.first_name}",
#             "Cita de terapia",
#             paciente.email
#         )

#         # Guardar los IDs de los eventos de Google Calendar
#         appointment.psicologo_event_id = psicologo_event_id
#         appointment.paciente_event_id = paciente_event_id
#         appointment.save()

#         return redirect('list_appointments')
#     return render(request, 'scheduling/book_appointment.html', {'schedule': schedule})

@login_required
def create_schedule(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time') 
        valor = request.POST.get('valor') 
        usuario = Usuario.objects.get(user=request.user)
        psico = Psicologo.objects.get(psi_idusuario=usuario)
         # Llama al método para crear el evento
        # calendar = GoogleCalendarManager()
        # calendar.create_event(summary, start_time, end_time, timezone, attendees)
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
    if request.method == "POST":
        meeting_uri= crear_espacio(request)
        if meeting_uri:
            scheduleid = request.POST.get('schedule_id') 
            agenda = Schedule.objects.get(schedule_id=scheduleid)
            appointed = Appointment.objects.get(schedule=agenda)
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

from django.utils import timezone


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

        # start_time = timezone.localtime(schedule.start_time)
        # end_time = timezone.localtime(schedule.end_time)

        # # # Asegúrate de que start_time y end_time sean objetos datetime
        # # if isinstance(start_time, str):
        # #     start_time = timezone.datetime.fromisoformat(start_time)
        # # if isinstance(end_time, str):
        # #     end_time = timezone.datetime.fromisoformat(end_time)

        # calendar = GoogleCalendarManager()

        # calendar.create_event(
        #     f"Cita con {paciente.pac_idusuario.user.first_name} {paciente.pac_idusuario.user.last_name}",
        #     start_time,
        #     end_time,
        #     schedule.psicologo.psi_idusuario.user.email
        # )

        # # Crear evento en Google Calendar para el paciente
        # calendar.create_event(
        #     f"Cita con Ps. {schedule.psicologo.psi_idusuario.user.first_name} {schedule.psicologo.psi_idusuario.user.last_name}",
        #     start_time,
        #     end_time,
        #     paciente.pac_idusuario.user.email
        # )

        # Guardar los IDs de los eventos de Google Calendar
        # appointment.psicologo_event_id = psicologo_event_id
        # appointment.paciente_event_id = paciente_event_id
        # appointment.save()

        return redirect('list_appointments')
    return render(request, 'scheduling/book_appointment.html', {'schedule': schedule})

@login_required
def list_appointments(request):
    usuario = Usuario.objects.get(user=request.user)
    paciente = Paciente.objects.get(pac_idusuario=usuario)
    appointments = Appointment.objects.filter(paciente=paciente)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        session_id = 'sessionId123'
        buy_order = 'buyOrder123'
        return_url = 'http://localhost:8000/payments/return/'

        try:
            response = transaction.create(buy_order, session_id, amount, return_url)
            # Ajustar según la estructura real de la respuesta
            url = response['url']  # Asegúrate de que la clave es correcta
            token = response['token']  # Asegúrate de que la clave es correcta
            return redirect(f"{url}?token_ws={token}")
        except TransbankError as e:
            return HttpResponse('Error: ' + str(e))

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

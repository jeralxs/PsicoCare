from django.shortcuts import render, redirect
from django.contrib import messages
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from googleapiclient.errors import HttpError
from .google_meet import GoogleMeetManager, obtener_credenciales
from .models import Sesion
from core.models import Usuario, Psicologo, Paciente
from scheduling.models import Schedule
# Create your views here.

def crear_espacio(request):
    creds = obtener_credenciales()
    meeting_uri = None

    try:
        print(f'Credenciales: {creds}')
        client = meet_v2.SpacesServiceClient(credentials=creds)
        request_body = meet_v2.CreateSpaceRequest()
        print(f'Request Body: {request}')
        response = client.create_space(request=request_body)
        print(f'Respuesta de la API: {response}')
        meeting_uri = response.meeting_uri
        print(f'Space created: {meeting_uri}')
    except Exception as error:
        # TODO(developer) - Handle errors from Meet API.
        print(f'An error occurred: {error}')
    return meeting_uri

def videollamada(request):
    usuario = Usuario.objects.get(user=request.user)
    if usuario.tipousuario == "psicologo":
        psico = Psicologo.objects.get(psi_idusuario=usuario)
        try:
            sesiones = Sesion.objects.filter(psicologo=psico.idpsicologo)
            return render(request, 'google_meet/videollamada.html',{'sesiones': sesiones})
        except Sesion.DoesNotExist:
            messages(request, 'No tienes sesiones programadas')
            return redirect('home')
    else:
        paciente = Paciente.objects.get(pac_idusuario=usuario)
        try:
            sesiones = Sesion.objects.filter(paciente=paciente.idpaciente)
        except Sesion.DoesNotExist:
            messages(request, 'No tienes sesiones programadas')
            return redirect('home')
        return render(request, 'google_meet/videollamada.html',{'sesiones': sesiones})
        
           

    

# def acceder_sesion(request, sesion_id):
#     sesion = Sesion.objects.get(id=sesion_id)
#     return render(request, 'google_meet/acceder_sesion.html', {'sesion': sesion})
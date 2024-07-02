from django.shortcuts import render
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from googleapiclient.errors import HttpError
from .google_meet import GoogleMeetManager, obtener_credenciales
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
    # mostrar si tiene links habilitados
    response = crear_espacio(request)
    return render(request, 'google_meet/videollamada.html', {'response': response})

    # meeting_uri = crear_espacio(request)
    # if meeting_uri:
    #     # Obtén el psicólogo y el paciente (puedes pasarlos como parámetros o obtenerlos del request)
    #     usuario = Usuario.objects.get(user=request.user)
    #     psicologo = Psicologo.objects.get(psi_idusuario=usuario)
    #     paciente = Paciente.objects.get(pac_idusuario=usuario)  # Obtén el paciente de alguna manera
        
    #     # Crea una nueva sesión con el meeting_uri
    #     sesion = Sesion.objects.create(
    #         psicologo=psicologo,
    #         paciente=paciente,
    #         meeting_uri=meeting_uri
    #     )
        
    #     return render(request, 'google_meet/videollamada.html', {'sesion': sesion})
    # else:
    #     return render(request, 'google_meet/error.html', {'message': 'No se pudo crear la videollamada'})

# def acceder_sesion(request, sesion_id):
#     sesion = Sesion.objects.get(id=sesion_id)
#     return render(request, 'google_meet/acceder_sesion.html', {'sesion': sesion})
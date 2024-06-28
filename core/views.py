from __future__ import print_function
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import FormRegistro, IngresarForm, DatosPersonalesForm,DatosProfesionalesForm, ResenaForm,PasswordResetForm,FormTestPaciente,Generopsicologo, FormularioMensaje, FormRegistroPsi, Tiposesion, Corrientepsicologica, Diagnostico, Motivosesion, Rangoprecio, Coberturasalud
from django.contrib import messages
from .models import Usuario, Test, Psicologo, puntaje_match
# from .google_meet import main, create_space
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.views.generic.edit import View
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Mensaje, Conversation

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from .google_calendar import GoogleCalendarManager, obtener_credenciales
from googleapiclient.errors import HttpError
from .google_meet import GoogleMeetManager, obtener_credenciales
from .models import Conversation

from django.shortcuts import render






def index(request):
    return render(request, 'core/index.html')

def resena(request):
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resena')
    else:
        form = ResenaForm()
    return render(request, 'core/resena.html')

def soporte(request):
    return render(request, 'core/soporte.html')

@login_required
def perfil(request):
    return render(request, 'core/perfil.html')

def test(request):
    if request.method == 'POST':
        form = FormTestPaciente(request.POST)
        if form.is_valid():
          
            test = form.save(commit=False) 

            if request.user.is_authenticated:
                usuario = Usuario.objects.get(user=request.user)
                test.idusuariotest_id = usuario.idusuario 
                test.save()    
           
            return redirect('matching', kwargs={'form_id': form.instance.id})
        else:
            print("Formulario no válido:")
            print(form.errors)
            print(request.POST)
    else:
        form = FormTestPaciente(request.POST)

    return render(request, 'core/test.html', {'form': form})


def matching(request):
    usuario = Usuario.objects.get(user=request.user)
    test = Usuario.objects.get(idusuariotest=usuario.idusuario)
    best_match = None
    highest_score = 0
    psicologos = Psicologo.objects.all()

    for psicologo in psicologos:
        score = puntaje_match(psicologo, test)
        if score > highest_score:
            highest_score = score
            best_match = psicologo

    return render(request, 'core/matching.html', best_match, highest_score)

# @login_required
# def matching(request, idtest):

#     best_match, score = encontrar_match(idtest)
#     return render(request, 'core/matching.html', {'best_match': best_match, 'score': score})


@login_required
def perfil_configurar(request):
    per_form = DatosPersonalesForm()
    prof_form = DatosProfesionalesForm()
    eliminar_form = EliminarForm()
    if request.method == 'POST':
        if 'edit_per' in request.POST:
            per_form = DatosPersonalesForm(request.POST)
            if per_form.is_valid():
                per_form.save() 
        if 'edit_prof' in request.POST:
            prof_form = DatosProfesionalesForm(request.POST)
            if prof_form.is_valid():
                prof_form.save()
        if 'eliminar_cuenta' in request.POST:
            eliminar_form = EliminarForm(request.POST)
            if eliminar_form.is_valid():
                eliminar_form.save()
    context = {
        'per_form': per_form,
        'prof_form': prof_form,
        'eliminar_form': eliminar_form,
    }
    return render(request, 'core/perfil_configurar.html', context=context) 


def registro(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu cuenta ha sido registrada exitosamente!')
            return redirect('ingresar')           
    else:
        form = FormRegistro()
        
    return render(request, 'core/registro.html', {'form': form})
def registro_psicologo(request):
    if request.method == 'POST':
        form = FormRegistroPsi(request.POST)
        if form.is_valid():
            messages.success(request, '¡Tu cuenta ha sido registrada exitosamente!')
            form.save()
            return redirect('ingresar')           
    else:
        form = FormRegistroPsi()
        
    return render(request, 'core/registro_psicologo.html', {'form': form})



def ingresar(request):
    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            Usuario2 = authenticate(username=username, password=password)
            if Usuario2:
                login(request, Usuario2)
                return redirect('home')
        else:
                messages.error(request, 'La cuenta o la contraseña no son correctas.')
    else:
        form = IngresarForm()
    
    return render(request, "core/ingresar.html", {'form':  IngresarForm()})

@login_required
def home(request):
    return render (request, "core/home.html")

def logout_view(request):
    logout(request)
    return redirect('index')


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
    response = crear_espacio(request)
    return render(request, 'core/videollamada.html', {'response': response})

def crear_sesion(request):
    if request.method == 'POST':
        summary = request.POST['summary']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        timezone = request.POST['timezone']
        attendees = request.POST.getlist('attendees')

        # Llama al método para crear el evento
        calendar = GoogleCalendarManager()
        calendar.create_event(summary, start_time, end_time, timezone, attendees)

        return HttpResponse('Sesión agendanda con éxito.')
    else:
        return render(request, 'core/crear_sesion.html')


def listar_sesiones(request):
    calendar = GoogleCalendarManager()
    sesiones = calendar.list_upcoming_events()
    
    # Filtrar las sesiones que aún existen
    sesiones_validas = []
    for sesion in sesiones:
        try:
            # Intentar acceder a la sesión en Google Calendar
            calendar.get_event_details(sesion['id'])
            # Si no se produce una excepción, la sesión aún existe
            sesiones_validas.append(sesion)
        except Exception as e:
            # Si se produce una excepción, la sesión ya no existe
            pass
    
    return render(request, 'core/listar_sesiones.html', {'sesiones': sesiones_validas})



def editar_sesion(request, event_id):
    # Obtener los detalles del evento
    calendar_manager = GoogleCalendarManager()
    event_details = calendar_manager.get_event_details(event_id)
    
    # Verificar si el método es POST (cuando se envía el formulario)
    if request.method == 'POST':
        # Resto del código para procesar el formulario...
        return HttpResponseRedirect(reverse('listar_sesiones'))
    else:
        # Renderizar el formulario de edición con los detalles del evento
        return render(request, 'core/editar_sesion.html', {'event_details': event_details})


def detalle_sesion(request, event_id):
    # Inicializar el administrador de Google Calendar
    calendar_manager = GoogleCalendarManager()

    # Obtener los detalles del evento con el event_id dado
    event_details = calendar_manager.get_event_details(event_id)
    # Renderizar la plantilla de detalle de sesión y pasar los detalles del evento
    return render(request, 'core/detalle_sesion.html', {'event_details': event_details})


def eliminar_sesion(request, event_id):
    # Inicializar el administrador de Google Calendar
    calendar_manager = GoogleCalendarManager()

    try:
        # Llama al método delete_event para eliminar el evento
        calendar_manager.delete_event(event_id)
        messages.success(request, 'El evento ha sido eliminado correctamente.')
    except HttpError as e:
        if e.resp.status == 410:
            messages.error(request, 'El evento ya ha sido eliminado.')
        else:
            messages.error(request, 'Ocurrió un error al eliminar el evento.')

    # Redirige a una página de confirmación
    return redirect(reverse('eliminar_sesion', args=[event_id]))

def recuperar_contrasena(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
        return render(request, 'core/recuperar_contrasena.html')
    else:
            form = PasswordResetForm()
    return render(request, 'core/recuperar_contrasena.html', {'form': form})

def pagos(request):
    return render(request, 'core/pagos.html')


@login_required
def chat_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.mensajes.all()
    return render(request, 'chat/chat.html', {'conversation': conversation, 'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        content = request.POST.get('content')

        if conversation_id and content:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            mensaje = Mensaje.objects.create(conversacion=conversation, autor=request.user, contenido=content)
            data = {
                'status': 'ok',
                'author': mensaje.autor.username,
                'content': mensaje.contenido,
                'timestamp': mensaje.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'error', 'message': 'Falta conversation_id o contenido'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})
    
def chat(request):
    mensajes = Mensaje.objects.all()  

    if request.method == 'POST':
        form = FormularioMensaje(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat')  
    else:
        form = FormularioMensaje()

    return render(request, 'core/chat.html', {'form': form, 'mensajes': mensajes})

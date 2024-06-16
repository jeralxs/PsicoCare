from __future__ import print_function
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import FormRegistro, IngresarForm, DatosPersonalesForm,DatosProfesionalesForm,EliminarForm,PasswordResetForm,FormTestPaciente
from django.contrib import messages
from .models import Usuario
#from .google_meet import main, create_space
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.views.generic.edit import View
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from transbank.error.transbank_error import TransbankError
from payments .webpay_config import transaction






import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.apps import meet_v2
# from .google_calendar import GoogleCalendarManager
# from googleapiclient.errors import HttpError
# from googleapiclient.discovery import build
# from google.oauth2 import service_account



def index(request):
    return render(request, 'core/index.html')
def perfil(request):
    return render(request, 'core/perfil.html')
def test(request):
    if request.method == 'POST':
        form = FormTestPaciente(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = FormTestPaciente()
    return render(request, 'core/test.html', {'form': form})

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

# def your_view(request):
#     stock_form = StockForm()
#     stock_history_form = StockHistoryForm() //added this
#     if request.method == 'POST':
#         stock_form = StockForm(request.POST)
#         stock_history_form == StockHistoryForm(request.POST)
#         if stock_form.is_valid() and stock_history_form.is_valid():
#             stock = stock_form.save() //changes here
#             stock_form_history.save(item_name=stock.item_name) //changes here
#             return HttpResponse("Saved")
#     return render(request, 'your_html.html', {'stock_form': stock_form, 'stock_history_form':stock_history_form})

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

def home(request):
    return render (request, "core/home.html")

def logout_view(request):
    logout(request)
    return redirect('index')

# SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

# def crear_espacio(request):
#     creds = None
#     meeting_uri = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)

#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:
#         client = meet_v2.SpacesServiceClient(credentials=creds)
#         request = meet_v2.CreateSpaceRequest()
#         response = client.create_space(request=request)
#         meeting_uri = response.meeting_uri
#         print(f'Space created: {meeting_uri}')
#     except Exception as error:
#         # TODO(developer) - Handle errors from Meet API.
#         print(f'An error occurred: {error}')
#     return meeting_uri

# def videollamada(request):
#     response = crear_espacio(request)
#     return render(request, 'core/videollamada.html', {'response': response})

 

# def crear_sesion(request):
#     if request.method == 'POST':
#         summary = request.POST['summary']
#         start_time = request.POST['start_time']
#         end_time = request.POST['end_time']
#         timezone = request.POST['timezone']
#         attendees = request.POST.getlist('attendees')

#         # Llama al método para crear el evento
#         calendar = GoogleCalendarManager()
#         calendar.create_event(summary, start_time, end_time, timezone, attendees)

#         return HttpResponse('Sesión agendanda con éxito.')
#     else:
#         return render(request, 'core/crear_sesion.html')


# def listar_sesiones(request):
#     calendar = GoogleCalendarManager()
#     sesiones = calendar.list_upcoming_events()
    
#     # Filtrar las sesiones que aún existen
#     sesiones_validas = []
#     for sesion in sesiones:
#         try:
#             # Intentar acceder a la sesión en Google Calendar
#             calendar.get_event_details(sesion['id'])
#             # Si no se produce una excepción, la sesión aún existe
#             sesiones_validas.append(sesion)
#         except Exception as e:
#             # Si se produce una excepción, la sesión ya no existe
#             pass
    
#     return render(request, 'core/listar_sesiones.html', {'sesiones': sesiones_validas})



# def editar_sesion(request, event_id):
#     # Obtener los detalles del evento
#     calendar_manager = GoogleCalendarManager()
#     event_details = calendar_manager.get_event_details(event_id)
    
#     # Verificar si el método es POST (cuando se envía el formulario)
#     if request.method == 'POST':
#         # Resto del código para procesar el formulario...
#         return HttpResponseRedirect(reverse('listar_sesiones'))
#     else:
#         # Renderizar el formulario de edición con los detalles del evento
#         return render(request, 'core/editar_sesion.html', {'event_details': event_details})


# def detalle_sesion(request, event_id):
#     # Inicializar el administrador de Google Calendar
#     calendar_manager = GoogleCalendarManager()

#     # Obtener los detalles del evento con el event_id dado
#     event_details = calendar_manager.get_event_details(event_id)
#     # Renderizar la plantilla de detalle de sesión y pasar los detalles del evento
#     return render(request, 'core/detalle_sesion.html', {'event_details': event_details})


# def eliminar_sesion(request, event_id):
#     # Inicializar el administrador de Google Calendar
#     calendar_manager = GoogleCalendarManager()

#     try:
#         # Llama al método delete_event para eliminar el evento
#         calendar_manager.delete_event(event_id)
#         messages.success(request, 'El evento ha sido eliminado correctamente.')
#     except HttpError as e:
#         if e.resp.status == 410:
#             messages.error(request, 'El evento ya ha sido eliminado.')
#         else:
#             messages.error(request, 'Ocurrió un error al eliminar el evento.')

#     # Redirige a una página de confirmación
#     return redirect(reverse('eliminar_sesion', args=[event_id]))

def recuperar_contrasena(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
        return render(request, 'core/recuperar_contrasena.html')
    else:
            form = PasswordResetForm()
    return render(request, 'core/recuperar_contrasena.html', {'form': form})


def init_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        session_id = 'sessionId'
        buy_order = 'buyOrder123'
        return_url = 'http://localhost:8000/payments/return/'

        try:
            response = transaction.create(buy_order, session_id, amount, return_url)
            return redirect(response.url + '?token_ws=' + response.token)
        except TransbankError as e:
            return HttpResponse('Error: ' + str(e))

    return render(request, 'payments/init_transaction.html')

def return_transaction(request):
    token = request.GET.get('token_ws')

    try:
        response = transaction.commit(token)
        return render(request, 'payments/success.html', {'response': response})
    except TransbankError as e:
        return HttpResponse('Error: ' + str(e))
from __future__ import print_function
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import FormRegistro, IngresarForm, EliminarForm, DatosPersonalesForm,DatosProfesionalesForm, ResenaForm,PasswordResetForm,FormTestPaciente,Generopsicologo, FormRegistroPsi, Tiposesion, Corrientepsicologica, Diagnostico, Motivosesion, Rangoprecio, Coberturasalud
from django.contrib import messages
from .models import Usuario, Test, Psicologo, puntaje_match, Pacientepsicologo, Paciente
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
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import SendMessageForm, ConversationForm

import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.apps import meet_v2
# from .google_calendar import GoogleCalendarManager, obtener_credenciales
# from googleapiclient.errors import HttpError
# from .google_meet import GoogleMeetManager, obtener_credenciales
from .models import Conversation
from scheduling.views import obtener_info_schedule
from scheduling.models import Appointment

from django.shortcuts import render






def index(request):
    return render(request, 'core/index.html')

def agendar(request):
    return render(request, 'core/agendar.html')

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
    usuario = Usuario.objects.get(user=request.user)
    if usuario.tipousuario == 'paciente':
        try:
            test = Test.objects.get(idusuariotest=usuario.idusuario)
            return render(request, 'core/perfil.html', {'test': test})
        except Test.DoesNotExist:
            return redirect('test')
    else:
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
           
            return redirect('matching')
        else:
            print("Formulario no válido:")
            print(form.errors)
            print(request.POST)
    else:
        form = FormTestPaciente(request.POST)

    return render(request, 'core/test.html', {'form': form})

def psicologo(request,psico_id,usu_id):
    context = obtener_info_psico(psico_id,usu_id)
    return render(request, 'core/psicologo.html', context)   
def obtener_info_psico(psico_id,usu_id):

    psicologo = Psicologo.objects.get(idpsicologo=psico_id)
    usuario = Usuario.objects.get(idusuario=usu_id)
    
    return {
        'id': psicologo.idpsicologo,
        'nombre': usuario.user.first_name,
        'apellido': usuario.user.last_name,
        'apellido_m': usuario.apellido_materno,
        'email': usuario.user.email,
        'genero': usuario.genero_idgenero.n_genero,
        'foto': usuario.foto,
        'telefono': usuario.telefono,
        'bio': psicologo.bio_info,
        'corriente': psicologo.corriente_idcorriente.corrientepsicologica,
        'tiposesion': psicologo.tiposesion_idtiposesion.nombre,
        'cobertura': psicologo.coberturasalud_id.coberturasalud,
        'preciomin': psicologo.rangoprecio_idrangoprecio.montominimo,
        'preciomax': psicologo.rangoprecio_idrangoprecio.montomaximo,
        'rangoetario': psicologo.rangoetario_idrangoetario.rangoetario,
        'diagnostico': psicologo.diagnostico_iddiagnostico.diagnostico,
        'motivosesion': psicologo.motivosesion_idmotivosesion.motivosesion,
    }

def matching(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        test = Test.objects.get(idusuariotest=usuario.idusuario)
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)
    except Test.DoesNotExist:
        return HttpResponse("Test no encontrado", status=404)
    
    psicologos = Psicologo.objects.all()
    puntuaciones = []

    for psicologo in psicologos:
        score = puntaje_match(psicologo, test)
        if score is not None:
            puntuaciones.append((psicologo, score, test))
    

    puntuaciones_ordenadas = sorted(puntuaciones, key=lambda x: x[1], reverse=True)
    
 
    mejores_opciones = puntuaciones_ordenadas[:5]

    context = {
        'mejores_opciones': mejores_opciones
    }

    return render(request, 'core/matching.html', context)


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
            user = form.save()
            apellido_materno = form.cleaned_data['apellido_materno']
            genero_idgenero = form.cleaned_data['genero_idgenero']
            Usuario.objects.create(
                usuario=user,
                tipousuario='paciente',
                apellido_materno=apellido_materno,
                genero_idgenero=genero_idgenero,
            )
            messages.success(request, 'Tu cuenta ha sido registrada con éxito')
            return redirect('ingresar')
    else:
        form = FormRegistro()
    
    return render(request, 'core/registro.html', {'form': form})


def registro_psicologo(request):
    if request.method == 'POST':
        form = FormRegistroPsi(request.POST)
        if form.is_valid():
            user = form.save()
            apellido_materno = form.cleaned_data['apellido_materno']
            genero_idgenero = form.cleaned_data['genero_idgenero']
            licencia = form.cleaned_data['licencia']
            Usuario.objects.create(
                usuario=user,
                tipousuario='psicologo',
                apellido_materno=apellido_materno,
                genero_idgenero=genero_idgenero,
                licencia=licencia,
            )
            messages.success(request, 'Tu cuenta ha sido registrada con éxito')
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
    usuario = Usuario.objects.get(user=request.user)
    if usuario.tipousuario == 'paciente':
        try:
            test = Test.objects.get(idusuariotest=usuario)
            paciente = Paciente.objects.get(pac_idusuario=usuario)
            psico = Pacientepsicologo.objects.filter(paciente_idusuario=paciente)
            psi = []
            for psico in psico:
                psi.append(psico)
            psicologo=psi[0]
            return render(request, 'core/home.html', {'psi': psicologo, 'test': test})
        except Pacientepsicologo.DoesNotExist:
            return redirect('index')
        except Test.DoesNotExist:
            return redirect('test')
    else:
        return render (request, "core/home.html")

def logout_view(request):
    logout(request)
    return redirect('index')




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

def pagos(request):
    return render(request, 'core/pagos.html')

@login_required
def chat_list(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    
    if usuario.tipousuario == 'psicologo':
        conversations = Conversation.objects.filter(psicologo__psi_idusuario=usuario)
    else:
        conversations = Conversation.objects.filter(paciente__pac_idusuario=usuario)
    
    return render(request, 'core/chat_list.html', {'conversations': conversations})

# @login_required
# def chat_view(request):
#     user = request.user
#     usuario = Usuario.objects.get(user=user)
#     user_type = 'psicologo' if usuario.tipousuario == 'psicologo' else 'paciente'
    
#     conversation_form = ConversationForm(user_type=user_type)
#     message_form = sendMessageForm()
    
#     current_conversation = None
#     messages = []

#     if request.method == 'POST':
#         if 'start_conversation' in request.POST:
#             conversation_form = ConversationForm(request.POST, user_type=user_type)
#             if conversation_form.is_valid():
#                 recipient = conversation_form.cleaned_data['recipient']
#                 if user_type == 'psicologo':
#                     psicologo = Psicologo.objects.get(psi_idusuario=usuario)
#                     paciente = recipient
#                 else:
#                     psicologo = recipient
#                     paciente = Paciente.objects.get(pac_idusuario=usuario)
                
#                 current_conversation, created = Conversation.objects.get_or_create(
#                     psicologo=psicologo,
#                     paciente=paciente
#                 )
#         elif 'send_message' in request.POST:
#             message_form = sendMessageForm(request.POST)
#             if message_form.is_valid():
#                 conversation_id = request.POST.get('conversation_id')
#                 current_conversation = get_object_or_404(Conversation, id=conversation_id)
#                 mensaje = message_form.save(commit=False)
#                 mensaje.conversation = current_conversation
#                 mensaje.usuario_idusuario = usuario
#                 mensaje.save()
                
#                 if request.is_ajax():
#                     return JsonResponse({
#                         'status': 'ok',
#                         'content': mensaje.contenido,
#                         'author': mensaje.usuario_idusuario.user.username,
#                         'timestamp': mensaje.timestamp.strftime('%d/%m/%Y %H:%M')
#                     })

#     if current_conversation:
#         messages = current_conversation.mensajes.all().order_by('timestamp')
    
#     # Obtenemos todas las conversaciones del usuario
#     if user_type == 'psicologo':
#         conversations = Conversation.objects.filter(psicologo__psi_idusuario=usuario)
#     else:
#         conversations = Conversation.objects.filter(paciente__pac_idusuario=usuario)

#     return render(request, 'core/chat.html', {
#         'conversation_form': conversation_form,
#         'message_form': message_form,
#         'current_conversation': current_conversation,
#         'messages': messages,
#         'conversations': conversations,
#     })

import traceback

@login_required
def chat_view(request):
    
    try:
        
        user = request.user
        usuario = get_object_or_404(Usuario, user=user)
        user_type = 'psicologo' if usuario.tipousuario == 'psicologo' else 'paciente'
        
        conversation_form = ConversationForm(user_type=user_type)
        message_form = SendMessageForm()
        
        current_conversation = None
        messages = []
    
        if request.method == 'POST':
            if 'start_conversation' in request.POST:
                conversation_form = ConversationForm(request.POST, user_type=user_type)
                if conversation_form.is_valid():
                    recipient = conversation_form.cleaned_data['recipient']
                    try:
                        if user_type == 'psicologo':
                            psicologo = get_object_or_404(Psicologo, psi_idusuario=usuario)
                            paciente = recipient
                        else:
                            psicologo = recipient
                            paciente = get_object_or_404(Paciente, pac_idusuario=usuario)
                        
                        current_conversation, created = Conversation.objects.get_or_create(
                            psicologo=psicologo,
                            paciente=paciente
                        )
                    except Exception as e:
                        print(f"Error starting conversation: {e}")
                        traceback.print_exc()
            elif 'send_message' in request.POST:
                try:
                    message_form = SendMessageForm(request.POST)
                    
                    if message_form.is_valid():
                        try:
                            conversation_id = request.POST.get('conversation_id')
                            current_conversation = get_object_or_404(Conversation, id=conversation_id)
                            mensaje = message_form.save(commit=False)
                            mensaje.conversation = current_conversation
                            mensaje.usuario_idusuario = usuario
                            mensaje.save()
                            
                            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                                return JsonResponse({
                                    'status': 'ok',
                                    'content': mensaje.contenido,
                                    'author': mensaje.usuario_idusuario.user.username,
                                    'timestamp': mensaje.fechahora.strftime('%d/%m/%Y %H:%M')
                                })
                        except Exception as e:
                            print(f"Error sending message: {e}")
                            traceback.print_exc()
                except Exception as e:
                        print(f"Error: {e}")
                        traceback.print_exc()

        if current_conversation:
            try:
                messages = current_conversation.mensaje_set.all().order_by('fechahora')
            except Exception as e:
                print(f"Error fetching messages: {e}")
                traceback.print_exc()
        
        try:
            if user_type == 'psicologo':
                conversations = Conversation.objects.filter(psicologo__psi_idusuario=usuario)
            else:
                conversations = Conversation.objects.filter(paciente__pac_idusuario=usuario)
        except Exception as e:
            print(f"Error fetching conversations: {e}")
            traceback.print_exc()

        return render(request, 'core/chat.html', {
            'conversation_form': conversation_form,
            'message_form': message_form,
            'current_conversation': current_conversation,
            'messages': messages,
            'conversations': conversations,
        })
    except Exception as e:
        print(f"Error in chat_view: {e}")
        traceback.print_exc()
        return render(request, 'core/error.html', {'message': 'An error occurred.'})




# def crear_espacio(request):
#     creds = obtener_credenciales()
#     meeting_uri = None

#     try:
#         print(f'Credenciales: {creds}')
#         client = meet_v2.SpacesServiceClient(credentials=creds)
#         request_body = meet_v2.CreateSpaceRequest()
#         print(f'Request Body: {request}')
#         response = client.create_space(request=request_body)
#         print(f'Respuesta de la API: {response}')
#         meeting_uri = response.meeting_uri
#         print(f'Space created: {meeting_uri}')
#     except Exception as error:
#         # TODO(developer) - Handle errors from Meet API.
#         print(f'An error occurred: {error}')
#     return meeting_uri

# def videollamada(request):
#     response = crear_espacio(request)
#     return render(request, 'core/videollamada.html', {'response': response})
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import index, perfil, registro, ingresar, home, recuperar_contrasena, perfil_configurar, test, videollamada, matching, pagos,chat, registro_psicologo
from core import views

urlpatterns = [
    path('', index, name='index'),
    path('perfil', perfil, name='perfil'),
    path('test', test, name='test'),
    path('perfil-configurar', perfil_configurar, name='perfil_configurar'),
    path('registro', registro, name='registro'),
    path('registro_psicologo', registro_psicologo, name='registro_psicologo'),
    path('ingresar', ingresar, name='ingresar'),
    path('home', home, name='home'),
    path('videollamada', videollamada, name='videollamada'),
    path('crear-sesion', views.crear_sesion, name='crear_sesion'),
    path('listar-sesiones', views.listar_sesiones, name='listar_sesiones'),
    path('editar-sesion/<str:event_id>/', views.editar_sesion, name='editar_sesion'),
    path('detalle-sesion/<str:event_id>/', views.detalle_sesion, name='detalle_sesion'),
    path('eliminar-sesion/<str:event_id>/', views.eliminar_sesion, name='eliminar_sesion'),
    path('recuperar_contrasena', recuperar_contrasena, name='recuperar_contrasena'),
    path('matching', matching, name='matching'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('pagos', pagos, name='pagos'),
    path('chat/<int:conversation_id>/', views.chat_view, name='chat_view'),
    path('send_message/', views.send_message, name='send_message'),
    path('chat', chat, name='chat'),
    path('logout', views.logout_view, name='logout'),


]
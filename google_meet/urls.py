from django.urls import path
from . import views

urlpatterns = [
    path('videollamada/', views.videollamada, name='videollamada'),
    # path('acceder_sesion/', views.acceder_sesion, name='acceder_sesion'),
]
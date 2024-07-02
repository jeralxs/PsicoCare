from django.urls import path
from .views import create_schedule, list_schedule, book_appointment, list_appointments, view_schedule

urlpatterns = [
    path('create_schedule/', create_schedule, name='create_schedule'),
    path('list_schedule/', list_schedule, name='list_schedule'),
    path('book_appointment/<schedule_id>/', book_appointment, name='book_appointment'),
    path('list_appointments/', list_appointments, name='list_appointments'),
    path('view_schedule/<psico_id>', view_schedule, name='view_schedule'),
]
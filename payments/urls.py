from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init_transaction, name='init_transaction'),
    path('return/', views.return_transaction, name='return_transaction'),
]
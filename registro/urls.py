# registro/urls.py
from django.urls import path
from . import views

app_name = 'registro'

urlpatterns = [
    path('novo/', views.iniciar_registro, name='iniciar_registro'),
    path('lista/', views.lista_registros, name='lista_registros'), # ADICIONE ESTA LINHA
]
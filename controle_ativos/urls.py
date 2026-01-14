from django.urls import path
from . import views

app_name = 'controle_ativos'

urlpatterns = [
    path('', views.lista_ativos, name='lista_ativos'),
    path('adicionar/', views.adicionar_ativo_chamado, name='adicionar_ativo_chamado'),
]

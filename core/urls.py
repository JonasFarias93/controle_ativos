from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('lojas/', views.lista_lojas, name='lista_lojas'),
    path('historico/', views.historico_movimentacoes, name='historico'), # Nova rota
]
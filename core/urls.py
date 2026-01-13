from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lojas/', views.lista_lojas, name='lista_lojas'),
]
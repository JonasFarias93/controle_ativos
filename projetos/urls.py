# projetos/urls.py
from django.urls import path
from . import views

app_name = 'projetos'
urlpatterns = [
    path('kit/novo/', views.cadastrar_kit, name='cadastrar_kit'),
    path('kit/editar/<int:kit_id>/', views.editar_kit, name='editar_kit'),
]
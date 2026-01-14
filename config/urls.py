from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ativos/', include('controle_ativos.urls')),
    path('', include('core.urls')), # Isso já engloba tudo que está no core
    path('registro/', include('registro.urls')),
    path('projetos/', include('projetos.urls')),
]
from django.contrib import admin
from .models import Categoria, Equipamento, AtivoFisico

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'tipo', 'exige_ativo')
    list_filter = ('categoria', 'exige_ativo')
    search_fields = ('nome', 'fabricante')

admin.site.register(Categoria)
from django.contrib import admin
from .models import Projeto, Kit, ItemKit

class ItemKitInline(admin.TabularInline):
    model = ItemKit
    # AQUI ESTAVA O ERRO: Mudamos de 'finalidade' para 'uso_no_kit'
    fields = ['equipamento', 'uso_no_kit', 'quantidade'] 
    extra = 1

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicio', 'ativo')

@admin.register(Kit)
class KitAdmin(admin.ModelAdmin): 
    list_display = ('nome', 'projeto')
    inlines = [ItemKitInline]
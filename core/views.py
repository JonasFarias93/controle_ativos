from django.shortcuts import render
from registro.models import ItemBipado # Importante para carregar os dados

def home(request):
    # Buscamos os itens para o Painel de Movimentações
    movimentacoes = ItemBipado.objects.select_related('registro', 'registro__loja', 'registro__projeto').all().order_by('-registro__data_registro')
    return render(request, 'core/home.html', {'movimentacoes': movimentacoes})

def lista_lojas(request):
    # Função temporária para evitar erro no link do menu
    return render(request, 'core/home.html') # Pode apontar para home por enquanto
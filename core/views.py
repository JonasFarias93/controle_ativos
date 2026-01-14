from django.shortcuts import render
from registro.models import ItemBipado, Loja # 1. Adicione 'Loja' no import

def home(request):
    movimentacoes = ItemBipado.objects.select_related('registro', 'registro__loja', 'registro__projeto').all().order_by('-registro__data_registro')
    return render(request, 'core/home.html', {'movimentacoes': movimentacoes})

def lista_lojas(request):
    # 2. Busque as lojas do banco de dados antes de passar para o render
    lojas = Loja.objects.all() 
    return render(request, 'core/lista_lojas.html', {'lojas': lojas})
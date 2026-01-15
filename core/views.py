from django.shortcuts import render
from django.db.models import Q
from registro.models import ItemBipado, Loja # 1. Adicione 'Loja' no import

def home(request):
    movimentacoes = ItemBipado.objects.select_related('registro', 'registro__loja', 'registro__projeto').all().order_by('-registro__data_registro')
    return render(request, 'core/home.html', {'movimentacoes': movimentacoes})

def lista_lojas(request):
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', 'filial') # Padrão é buscar por filial
    
    lojas = Loja.objects.all()

    if query:
        if tipo == 'filial':
            lojas = lojas.filter(filial__iexact=query)
        elif tipo == 'nome':
            lojas = lojas.filter(nome_filial__icontains=query)
        elif tipo == 'cnpj':
            lojas = lojas.filter(cnpj__icontains=query)
        elif tipo == 'cidade':
            lojas = lojas.filter(cidade__icontains=query)

    contexto = {
        'lojas': lojas.order_by('filial'),
        'query': query,
        'tipo': tipo,
        'total_registros': lojas.count(),
        'titulo': 'Relatório de Filiais Ativas'
    }
    return render(request, 'core/lista_lojas.html', contexto)
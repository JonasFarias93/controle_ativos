from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from registro.models import ItemBipado, Loja

def home(request):
    """View da Home com Dashboard simplificado"""
    # Pegamos apenas as 10 últimas movimentações para performance
    movimentacoes_recentes = ItemBipado.objects.select_related(
        'registro', 'registro__loja', 'registro__projeto'
    ).all().order_by('-registro__data_registro')[:10]
    
    contexto = {
        'movimentacoes': movimentacoes_recentes,
        'total_geral': ItemBipado.objects.count(),
        'hoje_count': ItemBipado.objects.filter(registro__data_registro__date=timezone.now().date()).count(),
    }
    return render(request, 'core/home.html', contexto)

def lista_lojas(request):
    """View de busca e relatório de lojas"""
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', 'filial') 
    
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


def historico_movimentacoes(request):
    """Exibe todas as movimentações com busca"""
    query = request.GET.get('q', '').strip()
    
    # Carrega tudo, mas permite buscar por Ativo ou Serial
    movimentacoes = ItemBipado.objects.select_related(
        'registro', 'registro__loja', 'registro__projeto'
    ).all().order_by('-registro__data_registro')

    if query:
        movimentacoes = movimentacoes.filter(
            Q(ativo_id__icontains=query) | 
            Q(num_serie__icontains=query) |
            Q(registro__loja__nome_filial__icontains=query)
        )

    return render(request, 'core/historico.html', {
        'movimentacoes': movimentacoes,
        'query': query
    })

def historico_movimentacoes(request):
    query = request.GET.get('q', '')
    
    # Aqui você busca os dados 
    movimentacoes = ItemBipado.objects.all().order_by('-id')

    if query:
        movimentacoes = movimentacoes.filter(item__nome__icontains=query)

    contexto = {
        'movimentacoes': movimentacoes,
        'query': query,
    }

    return render(request, 'core/historico.html', contexto)
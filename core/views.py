from django.shortcuts import render
from .models import Loja
from django.db.models import Q



def lista_lojas(request):
    query = request.GET.get('q')
    lojas = Loja.objects.all().order_by('filial')

    if query:
        try:
            filtro_int = int(query)
            lojas = lojas.filter(filial=filtro_int)
        except ValueError:
            lojas = lojas.filter(
                Q(nome_filial__icontains=query) |
                Q(endereco__icontains=query) |
                Q(cidade__icontains=query) |
                Q(cnpj__icontains=query)
            )

    context = {
        'titulo': 'Consulta de Lojas Ativas',
        'lojas': lojas,
        'total_registros': lojas.count(),
        'query': query or ''
    }
    return render(request, 'core/lista_lojas.html', context)

# Create your views here.

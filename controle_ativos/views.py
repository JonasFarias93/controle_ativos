from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import AtivoFisico  # Correto
from .forms import AtivoChamadoForm

def home(request):
    """View para a página inicial do sistema."""
    return render(request, 'core/home.html')

def lista_ativos(request):
    # Alterado de Ativo para AtivoFisico
    ativos_list = AtivoFisico.objects.all().order_by('-id') 
    form_novo_ativo = AtivoChamadoForm()    
    contexto = {
        'titulo_pagina': 'Controle de Ativos - Inventário',
        'ativos': ativos_list,
        'form': form_novo_ativo 
    }
    return render(request, 'controle_ativos/lista_ativos.html', contexto)

@require_POST
def adicionar_ativo_chamado(request):
    form = AtivoChamadoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('controle_ativos:lista') 
    
    # Alterado de Ativo para AtivoFisico
    ativos_list = AtivoFisico.objects.all()
    return render(request, 'controle_ativos/lista_ativos.html', {
        'ativos': ativos_list,
        'form': form,
        'erro': 'Verifique os dados preenchidos.'
    })
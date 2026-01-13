from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Ativo
from .forms import AtivoChamadoForm

def home(request):
    """View para a página inicial do sistema."""
    return render(request, 'core/home.html')

def lista_ativos(request):
    ativos_list = Ativo.objects.all().order_by('-id') # Mais recentes primeiro
    form_novo_ativo = AtivoChamadoForm()    
    contexto = {
        'titulo_pagina': 'Controle de Ativos - Inventário',
        'ativos': ativos_list,
        'form': form_novo_ativo # Enviando o form para o template
    }
    return render(request, 'controle_ativos/lista_ativos.html', contexto)

@require_POST
def adicionar_ativo_chamado(request):
    form = AtivoChamadoForm(request.POST)
    if form.is_valid():
        form.save()
        # CORREÇÃO: Usando o namespace 'controle_ativos' definido no seu urls.py
        return redirect('controle_ativos:lista') 
    
    # Se der erro, volta para a lista mostrando os erros do form
    ativos_list = Ativo.objects.all()
    return render(request, 'controle_ativos/lista_ativos.html', {
        'ativos': ativos_list,
        'form': form,
        'erro': 'Verifique os dados preenchidos.'
    })
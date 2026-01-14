from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import AtivoFisico
from .forms import AtivoChamadoForm

def home(request):
    """View para a página inicial do sistema."""
    return render(request, 'core/home.html')

def lista_ativos(request):
    # Otimizado com select_related para evitar múltiplas consultas ao banco (JOIN)
    ativos_list = AtivoFisico.objects.select_related('equipamento', 'equipamento__categoria').all().order_by('-id')
    
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
        try:
            form.save()
            messages.success(request, "Ativo cadastrado com sucesso!")
            return redirect('controle_ativos:lista')
        except Exception as e:
            # Captura erros que venham do método clean() do Model
            messages.error(request, f"Erro ao salvar: {e}")
    
    # Se o formulário for inválido ou der erro no save, recarrega a lista com os erros
    ativos_list = AtivoFisico.objects.select_related('equipamento').all().order_by('-id')
    return render(request, 'controle_ativos/lista_ativos.html', {
        'ativos': ativos_list,
        'form': form,
    })
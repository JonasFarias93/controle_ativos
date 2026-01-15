from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Projeto, Kit
from .forms import KitForm, ItemKitFormSet

def cadastrar_kit(request):
    """View para criar um novo Kit"""
    projetos = Projeto.objects.all().prefetch_related('kits__itens__equipamento')

    if request.method == 'POST':
        form = KitForm(request.POST)
        formset = ItemKitFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                kit = form.save()
                formset.instance = kit
                formset.save()
            messages.success(request, "Novo Kit cadastrado com sucesso!")
            return redirect('projetos:cadastrar_kit')
    else:
        form = KitForm()
        formset = ItemKitFormSet()

    return render(request, 'projetos/cadastrar_kit.html', {
        'projetos': projetos,
        'form': form,
        'formset': formset,
        'editando': False
    })

def editar_kit(request, kit_id):
    """View específica para editar um Kit existente"""
    kit = get_object_or_404(Kit, id=kit_id)
    projetos = Projeto.objects.all().prefetch_related('kits__itens__equipamento')

    if request.method == 'POST':
        form = KitForm(request.POST, instance=kit)
        formset = ItemKitFormSet(request.POST, instance=kit)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, f"Kit '{kit.nome}' atualizado!")
            return redirect('projetos:cadastrar_kit')
    else:
        form = KitForm(instance=kit)
        formset = ItemKitFormSet(instance=kit)

    return render(request, 'projetos/cadastrar_kit.html', {
        'projetos': projetos,
        'form': form,
        'formset': formset,
        'editando': True,
        'kit': kit
    })
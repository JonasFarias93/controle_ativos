from django.shortcuts import render, redirect, get_object_or_404
from .forms import KitForm, ItemKitFormSet
from django.shortcuts import render
from .models import Projeto, Kit  # Certifique-se de que os nomes dos models estão corretos

def lista_projetos(request):
    # Carrega os projetos e já traz os kits vinculados a eles
    projetos = Projeto.objects.all().prefetch_related('kits') 
    return render(request, 'projetos/lista_projetos.html', {'projetos': projetos})

# projetos/views.py
def cadastrar_kit(request):
    # Parte 1: Busca dados para a listagem (topo da página)
    projetos = Projeto.objects.all().prefetch_related('kits__itens') # Carrega kits e itens

    # Parte 2: Lógica do Formulário (base da página)
    if request.method == 'POST':
        form = KitForm(request.POST)
        formset = ItemKitFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            kit = form.save()
            formset.instance = kit
            formset.save()
            return redirect('projetos:cadastrar_kit') # Recarrega a página para limpar o form e mostrar o novo kit
    else:
        form = KitForm()
        formset = ItemKitFormSet()

    return render(request, 'projetos/cadastrar_kit.html', {
        'projetos': projetos,
        'form': form,
        'formset': formset
    })


def editar_kit(request, kit_id):
    kit = get_object_or_404(Kit, id=kit_id)
    
    if request.method == 'POST':
        form = KitForm(request.POST, instance=kit)
        formset = ItemKitFormSet(request.POST, instance=kit)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('projetos:cadastrar_kit')
    else:
        form = KitForm(instance=kit)
        formset = ItemKitFormSet(instance=kit)
    
    projetos = Projeto.objects.all().prefetch_related('kits__itens')
    
    return render(request, 'projetos/cadastrar_kit.html', {
        'form': form,
        'formset': formset,
        'editando': True,
        'kit': kit,
        'projetos': projetos
    })
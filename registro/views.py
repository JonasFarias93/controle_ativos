from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroSaidaForm
from .models import RegistroSaida, ItemBipado
from projetos.models import Kit

def iniciar_registro(request):
    # Captura o ID do kit que vem da URL (enviado pelo seu JavaScript atualizarKit)
    kit_id = request.GET.get('kit')
    kit_selecionado = None
    if kit_id:
        kit_selecionado = get_object_or_404(Kit, id=kit_id)

    if request.method == 'POST':
        form = RegistroSaidaForm(request.POST)
        if form.is_valid():
            # 1. Salva o Registro Pai
            registro_instancia = form.save(commit=False)
            registro_instancia.tecnico = request.user
            registro_instancia.save()

            # 2. Pega as listas de bipes que o seu segundo HTML enviou
            tipos = request.POST.getlist('tipo_equipamento[]')
            ativos = request.POST.getlist('ativo[]')
            series = request.POST.getlist('serie[]')

            # 3. Salva os bipes no banco de dados
            for t, a, s in zip(tipos, ativos, series):
                if t: # Verifica se não está vazio
                    ItemBipado.objects.create(
                        registro=registro_instancia,
                        equipamento_tipo=t,
                        ativo_id=a,
                        num_serie=s,
                        codigo_java="GERADO" # Ou sua lógica de mapeamento
                    )
            
            return redirect('home')
    else:
        form = RegistroSaidaForm()
        # Se veio um kit pela URL, já pré-seleciona ele no formulário
        if kit_id:
            form.fields['kit_utilizado'].initial = kit_id

    # IMPORTANTE: Passamos o 'kit' para o template reconhecer e liberar a tabela de bipes
    return render(request, 'registro/form_registro.html', {
        'form': form, 
        'kit': kit_selecionado
    })

def tela_bipagem(request, registro_id):
    registro = get_object_or_404(RegistroSaida, id=registro_id)
    # Pegamos apenas os itens desse registro que ainda não foram bipados ou precisam de correção
    itens = ItemBipado.objects.filter(registro=registro)
    
    if request.method == 'POST':
        # Lógica para salvar os bipes vindo do formulário
        for item in itens:
            ativo = request.POST.get(f'ativo_{item.id}')
            serie = request.POST.get(f'serie_{item.id}')
            if ativo and serie:
                item.ativo_id = ativo
                item.num_serie = serie
                item.save()
        return redirect('home')

    return render(request, 'registro/tela_bipagem.html', {'registro': registro, 'itens': itens})

def lista_registros(request):
    itens = ItemBipado.objects.select_related(
        'registro', 
        'registro__projeto', 
        'registro__loja'
    ).all().order_by('-registro__data_registro')
    return render(request, 'registro/lista_registros.html', {'itens': itens})
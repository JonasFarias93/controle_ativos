from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroSaidaForm
from .models import RegistroSaida, ItemBipado
from projetos.models import Kit

def iniciar_registro(request):
    if request.method == 'POST':
        form = RegistroSaidaForm(request.POST)
        if form.is_valid():
            # 1. Primeiro salva o Registro (Pai)
            registro_instancia = form.save(commit=False)
            registro_instancia.tecnico = request.user
            registro_instancia.save()

            # 2. Pega os dados dos itens bipados
            tipos = request.POST.getlist('tipo_equipamento[]')
            ativos = request.POST.getlist('ativo[]')
            series = request.POST.getlist('serie[]')

            # 3. Mapeamento simples para o código JAVA (pode expandir depois)
            mapeamento_java = {
                'Monitor LCD (LCD)': 'JAV-MON-01',
                'Micro (CPU)': 'JAV-CPU-02',
                'Leitor Cod.Barras (Com Fio)': 'JAV-LEI-03',
            }

            # 4. Salva cada item bipado vinculado ao registro acima
            for t, a, s in zip(tipos, ativos, series):
                # Aqui você define o JAVA baseado no tipo
                java_detectado = mapeamento_java.get(t, 'N/A')
                
                ItemBipado.objects.create(
                    registro=registro_instancia, # Aqui a variável correta
                    equipamento_tipo=t,
                    ativo_id=a,
                    num_serie=s,
                    codigo_java=java_detectado # Certifique-se que esse campo existe no model
                )
            
            return redirect('home')
    else:
        form = RegistroSaidaForm()
    
    return render(request, 'registro/form_registro.html', {'form': form})

def lista_registros(request):
    # Buscamos todos os itens bipados para montar a tabela detalhada
    itens = ItemBipado.objects.select_related('registro', 'registro__projeto', 'registro__loja').all().order_by('-registro__data_registro')
    
    # registro/views.py
    return redirect('home') # 'home' costuma ser o nome da rota no core/urls.py


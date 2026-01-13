# Arquivo: controle_ativos/forms.py

from django import forms
from django.utils import timezone
from .models import Ativo, Chamado
from projetos.models import Categoria
from django.db import transaction

# Crie uma tupla de campos que o usuário não precisa ver no Chamado
CHAMADO_FIELDS_EXCLUIDOS = ('smartx', 'volume', 'data_saida') 

class AtivoChamadoForm(forms.ModelForm):
    """
    Formulário para criar um novo Ativo e seu Chamado associado.
    """
    
    # ----------------------------------------------------
    # CAMPOS DO CHAMADO (Definidos explicitamente)
    # ----------------------------------------------------
    # O campo 'categoria' agora é obrigatório
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoria/Projeto",
        empty_label="Selecione a Categoria",
        help_text="O projeto e categoria a que este chamado pertence."
    )
    
    # Campo 'numero_chamado'
    numero_chamado = forms.CharField(
        max_length=50,
        label="Chamado / Nº",
        help_text="Número único do chamado ou requisição."
    )
    
    # O campo 'data_separacao' será preenchido automaticamente, mas definimos o CharField aqui 
    # para que o usuário veja a informação ou para fins de validação no futuro.
    data_separacao = forms.DateField(
        label="Data Separação",
        initial=timezone.localdate,
        disabled=True # Impede o usuário de alterar, garantindo que seja a data de criação
    )
    
    # ----------------------------------------------------
    # CAMPOS DO ATIVO (Definidos no Meta)
    # ----------------------------------------------------
    
    class Meta:
        model = Ativo
        # Campos do Ativo que o usuário irá preencher
        fields = ('tipo', 'codigo_equipamento', 'nr_serie', 'ativo_id', 'status')
        
    # O método clean garante que os dados sejam validados
    def clean(self):
        cleaned_data = super().clean()
        # Aqui, você pode adicionar validações complexas, como checar se o numero_chamado já existe.
        return cleaned_data
        
    @transaction.atomic
    def save(self, commit=True):
        # 1. Salvar o Chamado primeiro
        categoria = self.cleaned_data.pop('categoria')
        numero_chamado = self.cleaned_data.pop('numero_chamado')
        
        # Cria o objeto Chamado
        chamado_novo = Chamado.objects.create(
            categoria=categoria,
            numero_chamado=numero_chamado,
            data_separacao=timezone.localdate(), # <--- Padrão: data de hoje (dia da criação)
            smartx='A_AGUARDANDO', # Status inicial padrão
            volume=1 # Um ativo = um volume, simplificando
        )
        
        # 2. Salvar o Ativo
        ativo = super().save(commit=False)
        ativo.chamado = chamado_novo # Vincula o Ativo ao Chamado recém-criado
        
        if commit:
            ativo.save()
            
        return ativo
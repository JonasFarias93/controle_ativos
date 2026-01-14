# Arquivo: controle_ativos/forms.py
from django import forms
from .models import AtivoFisico

class AtivoChamadoForm(forms.ModelForm):
    """
    Formulário simplificado para destravar o sistema e permitir
    o cadastro de Ativos Físicos vinculados aos Equipamentos.
    """
    class Meta:
        model = AtivoFisico
        fields = ['equipamento', 'patrimonio_ativo', 'num_serie', 'status']
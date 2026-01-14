from django import forms
from .models import RegistroSaida, ItemBipado
from core.models import Loja
from projetos.models import Kit, Projeto

class RegistroSaidaForm(forms.ModelForm):
    class Meta:
        model = RegistroSaida
        fields = ['projeto', 'loja', 'kit_utilizado', 'numero_chamado']
        widgets = {
            'numero_chamado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: RITM0123456'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
            'loja': forms.Select(attrs={'class': 'form-select'}),
            'kit_utilizado': forms.Select(attrs={'class': 'form-select'}),
        }
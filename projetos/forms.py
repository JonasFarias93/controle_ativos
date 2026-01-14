from django import forms
from .models import Kit, ItemKit
from django.forms import inlineformset_factory

class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ['nome', 'projeto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Kit PDV Padrão'}),
            'projeto': forms.Select(attrs={'class': 'form-control'}),
        }

ItemKitFormSet = inlineformset_factory(
    Kit, ItemKit,
    fields=['equipamento', 'uso_no_kit', 'quantidade'],
    extra=1,
    can_delete=True,
    widgets={
        'equipamento': forms.Select(attrs={'class': 'form-select'}),
        'uso_no_kit': forms.Select(attrs={'class': 'form-select'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    }
)
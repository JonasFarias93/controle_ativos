from django import forms
from .models import AtivoFisico

class AtivoChamadoForm(forms.ModelForm):
    class Meta:
        model = AtivoFisico
        fields = ['equipamento', 'patrimonio_ativo', 'num_serie', 'status']
        
        # Injetando classes CSS 
        widgets = {
            'equipamento': forms.Select(attrs={'class': 'form-select'}),
            'patrimonio_ativo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: PAT-2024-001'}),
            'num_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Série'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_patrimonio_ativo(self):
        """Garante que o patrimônio seja salvo sempre em maiúsculas e valida unicidade."""
        patrimonio = self.cleaned_data.get('patrimonio_ativo')
        if patrimonio:
            patrimonio = patrimonio.upper()
            # Verifica se já existe, ignorando o próprio objeto caso seja uma edição
            if AtivoFisico.objects.filter(patrimonio_ativo=patrimonio).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este número de patrimônio já está cadastrado no sistema.")
        return patrimonio

    def clean(self):
        """
        Validação cruzada: Reforça a regra do Model no nível do formulário
        para evitar que o erro chegue ao banco de dados.
        """
        cleaned_data = super().clean()
        equipamento = cleaned_data.get('equipamento')
        patrimonio = cleaned_data.get('patrimonio_ativo')
        num_serie = cleaned_data.get('num_serie')

        if equipamento and equipamento.exige_ativo:
            if not patrimonio and not num_serie:
                msg = "Este equipamento exige Patrimônio ou Número de Série."
                self.add_error('patrimonio_ativo', msg)
                self.add_error('num_serie', msg)
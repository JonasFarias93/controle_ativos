from django.db import models
from controle_ativos.models import Equipamento 

class Projeto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    # ESTES SÃO OS CAMPOS QUE ESTÃO FALTANDO:
    data_inicio = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Kit(models.Model):
    nome = models.CharField(max_length=100)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='kits')
    
    def __str__(self):
        return f"{self.projeto.nome} - {self.nome}"

class ItemKit(models.Model):
    OCASIAO_CHOICES = [
        ('pdv', 'PDV'),
        ('tc', 'Terminal de Consulta (TC)'),
        ('hibrido', 'Híbrido (PDV + TC)'),
        ('gerencia', 'Gerência'),
        ('farmacia', 'Farmácia'),
        ('outro', 'Outro'),
    ]

    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name='itens')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT)
    
    # Verifique se o nome aqui é 'uso_no_kit'
    uso_no_kit = models.CharField(
        max_length=50, 
        choices=OCASIAO_CHOICES,
        default='pdv'
    )
    
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.equipamento.nome} ({self.get_uso_no_kit_display()})"
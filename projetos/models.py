from django.db import models
from controle_ativos.models import Equipamento 

class Projeto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data_inicio = models.DateField(auto_now_add=True, verbose_name="Data de Início")
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Kit(models.Model):
    nome = models.CharField(max_length=100)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='kits')
    
    class Meta:
        verbose_name = "Kit"
        verbose_name_plural = "Kits"
        ordering = ['projeto', 'nome']

    def __str__(self):
        return f"{self.projeto.nome} - {self.nome}"

    @property
    def total_pecas(self):
        """Retorna a soma das quantidades de todos os itens do kit"""
        return sum(item.quantidade for item in self.itens.all())

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
    uso_no_kit = models.CharField(
        max_length=50, 
        choices=OCASIAO_CHOICES,
        default='pdv',
        verbose_name="Ocasião de Uso"
    )
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Item do Kit"
        verbose_name_plural = "Itens do Kit"
        # Impede duplicar o mesmo equipamento para o mesmo uso no mesmo kit
        unique_together = ('kit', 'equipamento', 'uso_no_kit')

    def __str__(self):
        return f"{self.quantidade}x {self.equipamento.nome} ({self.get_uso_no_kit_display()})"
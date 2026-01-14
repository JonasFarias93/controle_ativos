from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT) # PROTECT evita deletar categoria com itens
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, help_text="Ex: LCD, Touch, Laser")
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    exige_ativo = models.BooleanField(
        default=True, 
        verbose_name="Possui Patrimônio?",
        help_text="Marque apenas se o item tiver etiqueta de patrimônio"
    )

    class Meta:
        verbose_name = "Modelo de Equipamento"
        verbose_name_plural = "Modelos de Equipamentos"

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class AtivoFisico(models.Model):
    # Usando TextChoices para facilitar filtros e legibilidade
    class StatusAtivo(models.TextChoices):
        ESTOQUE = 'estoque', 'Em Estoque'
        ENVIADO = 'enviado', 'Enviado'
        DEFEITO = 'defeito', 'Com Defeito'
        MANUTENCAO = 'manutencao', 'Em Manutenção'

    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='ativos')
    patrimonio_ativo = models.CharField(max_length=100, unique=True, blank=True, null=True)
    num_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=1) 
    data_cadastro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=StatusAtivo.choices,
        default=StatusAtivo.ESTOQUE
    )

    class Meta:
        verbose_name = "Ativo Físico"
        verbose_name_plural = "Ativos Físicos"

    def clean(self):
        """Validação personalizada: Se exige_ativo for True, exige patrimônio ou serial."""
        if self.equipamento.exige_ativo and not (self.patrimonio_ativo or self.num_serie):
            raise ValidationError(
                "Para este equipamento, é obrigatório informar o Patrimônio ou o Número de Série."
            )

    def __str__(self):
        if self.equipamento.exige_ativo:
            return f"{self.patrimonio_ativo or 'S/N'} - {self.equipamento.nome}"
        return f"{self.equipamento.nome} (Qtd: {self.quantidade})"
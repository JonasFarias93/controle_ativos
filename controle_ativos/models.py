from django.db import models
from projetos.models import Categoria

# --- DEFINIÇÃO DOS CHOICES ---

# 1. Choices para o Status do Processo de Movimentação (SMARTX)
SMARTX_CHOICES = [
    ('A_SEPARACAO', 'A. Separação'),
    ('A_NF', 'A. NF'),
    ('A_COLETA', 'A. Coleta'),
    ('A_BAIXA', 'A. Baixa'),
    ('FINALIZADO', 'Finalizado'),
]

# 2. Choices para o Status Físico/Localização do Equipamento (STATUS)
STATUS_CHOICES = [
    ('ESTOQUE', 'Em Estoque'),
    ('USO', 'Em Uso'),
    ('BAIXA', 'Baixado'),
    ('MOVIMENTACAO', 'Em Movimentação'),
]

# ------------------------------

### 1. Modelo TipoEquipamento
class TipoEquipamento(models.Model):
    """Armazena a descrição padronizada dos equipamentos."""
    nome = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Tipo de Equipamento"
    )
    
    class Meta:
        verbose_name = "Tipo de Equipamento"
        verbose_name_plural = "Tipos de Equipamento"
        
    def __str__(self):
        return self.nome
        

### 2. Modelo Chamado (SMARTX CORRIGIDO)
class Chamado(models.Model):
    """Armazena os detalhes do chamado/requisição de movimentação."""
    numero_chamado = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Chamado / Nº"
    )
    data_separacao = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Data Separação"
    )
    data_saida = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Data Saída"
    )
    
    # CORREÇÃO: Aplicando SMARTX_CHOICES e definindo um default
    smartx = models.CharField(
        max_length=50, 
        choices=SMARTX_CHOICES,
        default='A_AGUARDANDO',
        verbose_name="Smartx / Status do Chamado"
    )
    
    volume = models.IntegerField(
        verbose_name="Volume"
    )

    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT, 
        verbose_name="Categoria do Projeto"
    )
    
    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        
    def __str__(self):
        return self.numero_chamado
        
### 3. Modelo Ativo (STATUS MANTIDO)
class Ativo(models.Model):
    """Armazena o registro de cada equipamento individual (ativo)."""
    
    # Relacionamentos
    chamado = models.ForeignKey(
        Chamado, 
        on_delete=models.SET_NULL,
        null=True, 
        verbose_name="Chamado Associado"
    )
    tipo = models.ForeignKey(
        TipoEquipamento, 
        on_delete=models.PROTECT,
        verbose_name="Tipo"
    )

    # Campos do Ativo
    codigo_equipamento = models.CharField(
        max_length=50, 
        verbose_name="C. Equipamento"
    )
    nr_serie = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nº de Série"
    )
    ativo_id = models.CharField(
        max_length=50, 
        verbose_name="ID Ativo",
        blank=True,
        null=True
    )

    # STATUS MANTIDO
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ESTOQUE',
        verbose_name="Status Atual"
    )

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"

    def __str__(self):
        return f'{self.tipo.nome} ({self.nr_serie})'
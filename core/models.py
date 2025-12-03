# Seu código de modelo aqui (conforme fornecido anteriormente)

from django.db import models

# =================================================================
# 1. MODELO LOJA 
# =================================================================

class Loja(models.Model):
    # CHAVE PRINCIPAL: Único e identifica a loja (Java/Filial)
    filial = models.IntegerField(
        unique=True,
        primary_key=True,
        verbose_name="Código Filial (Java/ID)"
    )
    
    # DADOS OBTIDOS DO AUTOCOM
    nome_filial = models.CharField(max_length=150, verbose_name="Nome da Filial")
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, verbose_name="UF")
    telefone = models.CharField(max_length=20, null=True, blank=True)
    ip_banco_12 = models.CharField(max_length=20, null=True, blank=True, verbose_name="IP Banco 12")
    hist = models.CharField(max_length=50, null=True, blank=True)
    logomarca = models.CharField(max_length=20, null=True, blank=False)

    # STATUS E REPRESENTAÇÃO
    STATUS_CHOICES = [
        ('ATIVA', 'Ativa'),
        ('ABERTURA', 'Em Abertura'),
        ('INATIVA', 'Inativa'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ATIVA'
    )

    def __str__(self):
        return f"{self.filial} - {self.nome_filial}"
    
    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"

# =================================================================
# 2. MODELO PROJETO
# =================================================================

class Projeto(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

# =================================================================
# 3. MODELO ITEMBASE 
# =================================================================

class ItemBase(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Equipamento/Kit")
    descricao = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=50, default='PDV', help_text="Ex: PDV, Redes, Periférico, Servidor")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Item Base"
        verbose_name_plural = "Itens Base"
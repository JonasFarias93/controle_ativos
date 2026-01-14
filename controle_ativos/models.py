from django.db import models

class Categoria(models.Model):
    """ Ex: Monitor, Micro, Rede, Periféricos """
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    """ 
    Ficha Cadastral: Onde você define o padrão do que existe.
    """
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50) # Ex: LCD, Touch, Laser
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    
    # A regra que você pediu:
    exige_ativo = models.BooleanField(default=True, verbose_name="Este item possui Ativo/Patrimônio?")
    
    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class AtivoFisico(models.Model):
    """
    O estoque real: Onde ocorre o "Bip".
    """
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    
    # Identificadores Únicos
    patrimonio_ativo = models.CharField(max_length=100, unique=True, blank=True, null=True)
    num_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    # Controle de quantidade para itens sem ativo (ex: Hub USB)
    quantidade = models.PositiveIntegerField(default=1) 
    
    data_cadastro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, 
        choices=[('estoque', 'Em Estoque'), ('enviado', 'Enviado'), ('defeito', 'Defeito')],
        default='estoque'
    )

    def __str__(self):
        if self.equipamento.exige_ativo:
            return f"Ativo: {self.patrimonio_ativo} - {self.equipamento.nome}"
        return f"{self.equipamento.nome} (Qtd: {self.quantidade})"
from django.db import models
from django.contrib.auth.models import User
from core.models import Loja
from projetos.models import Kit, Projeto

# registro/models.py
class RegistroSaida(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    kit_utilizado = models.ForeignKey(Kit, on_delete=models.PROTECT)
    numero_chamado = models.CharField(max_length=50, verbose_name="Número do Chamado / Pedido") # NOVO
    observacoes = models.TextField(blank=True, null=True) # NOVO
    data_registro = models.DateTimeField(auto_now_add=True)
    tecnico = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Chamado {self.numero_chamado} - {self.loja.nome}"

class ItemBipado(models.Model):
    registro = models.ForeignKey(RegistroSaida, related_name='itens_bipados', on_delete=models.CASCADE)
    equipamento_tipo = models.CharField(max_length=100)
    ativo_id = models.CharField(max_length=100, verbose_name="Ativo ID") # Prioridade
    num_serie = models.CharField(max_length=100, verbose_name="Número de Série")
    codigo_java = models.CharField(max_length=20, blank=True, null=True)
    # Campos como 'JAVA' ou 'C.EQUIPAMENTO' podem ser derivados do cadastro de ativos se necessário
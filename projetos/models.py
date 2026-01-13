from django.db import models

class Projeto(models.Model):
    """Modelo principal: Adição, Rollout, Abertura."""
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Projeto")
    
    class Meta:
        verbose_name = "Projeto Principal"
        verbose_name_plural = "Projetos Principais"

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    """Modelo filho: Sala sua Saúde, Kit TC, etc."""
    # Chave Estrangeira: vincula esta categoria ao seu Projeto Principal
    projeto = models.ForeignKey(
        Projeto, 
        on_delete=models.CASCADE, 
        related_name='categorias',
        verbose_name="Projeto Principal"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")

    class Meta:
        verbose_name = "Categoria de Projeto"
        verbose_name_plural = "Categorias de Projetos"
        unique_together = ('projeto', 'nome') # Garante que uma categoria seja única por projeto

    def __str__(self):
        return f'{self.nome} ({self.projeto.nome})'
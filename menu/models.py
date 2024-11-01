from django.db import models

class Tarefa(models.Model):
    CATEGORIAS = [
        ('urgente', 'Urgente'),
        ('proximo', 'Está Próximo'),
        ('distante', 'Distante')
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
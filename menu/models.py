from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    PRIORIDADE_CHOICES = [
        ('urgente', 'Urgente'),
        ('proximo', 'Próximo'),
        ('distante', 'Distante'),
    ]
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20)
    concluida = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='distante')  # Novo campo

    def __str__(self):
        return self.titulo

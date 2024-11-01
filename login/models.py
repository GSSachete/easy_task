from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento com User
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)  # Nome de usuário adicional
    escolaridade = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    escola = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome
from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    escolaridade = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    escola = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
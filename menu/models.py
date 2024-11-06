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
    participantes = models.ManyToManyField('login.Usuario', related_name="tarefas")
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='distante')
    arquivo = models.FileField(upload_to='tarefas_arquivos/', blank=True, null=True)  

    def __str__(self):
        return self.titulo


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
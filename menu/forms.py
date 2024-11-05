from django import forms
from login.models import Usuario
from .models import Tarefa



class TarefaForm(forms.ModelForm):
    participantes = forms.CharField(
        required=False,
        help_text="Digite os nomes de usuário dos participantes, separados por vírgula"
    )

    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'categoria', 'prioridade', 'participantes']


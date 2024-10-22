from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import DateInput
from .models import Usuario  # Substitua YourModel por Usuario
from django import forms

class RegisterForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario
        fields = ['nome', 'escolaridade', 'data_nascimento', 'escola', 'email', 'senha']

class RegisterForm(forms.ModelForm):
    data_nascimento = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario
        fields = ['nome', 'escolaridade', 'data_nascimento', 'escola', 'email', 'senha']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Usuario')
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegisterForm(forms.Form):
    NIVEIS_ESCOLARIDADE = [
        ('0', 'Primário'),
        ('1', 'Ensino Fundamental'),
        ('2', 'Ensino Médio'),
        ('3', 'Ensino Técnico'),
        ('4', 'Ensino Superior'),
        ('5', 'Pós-graduação'),
        ('6', 'Mestrado'),
        ('7', 'Doutorado'),
    ]


    nome = forms.CharField(max_length=100)
    escolaridade = forms.ChoiceField(choices=NIVEIS_ESCOLARIDADE)
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    escola = forms.CharField(max_length=100)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
    
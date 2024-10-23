from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import DateInput
from .models import Usuario  # Substitua YourModel por Usuario
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Usuario')
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegisterForm(UserCreationForm):
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
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            usuario = Usuario.objects.create(
                user=user,
                escolaridade=self.cleaned_data['escolaridade'],
                data_nascimento=self.cleaned_data['data_nascimento'],
                escola=self.cleaned_data['escola']
            )
            usuario.save()
        return user
    
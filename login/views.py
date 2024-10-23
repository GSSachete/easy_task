from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .models import Usuario

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('menu')  # Redireciona para o menu após o login
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def save(self, commit=True):
    print("Salvando o formulário...")  # Adiciona um print para verificar se o save é chamado
    user = super(RegisterForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    print(f"Dados do usuário: {user.username}, {user.email}")  # Exibe os dados sendo salvos no User
    if commit:
        user.save()
        print("Usuário salvo com sucesso.")
        usuario = Usuario.objects.create(
            user=user,
            nome=self.cleaned_data['nome'],
            escolaridade=self.cleaned_data['escolaridade'],
            data_nascimento=self.cleaned_data['data_nascimento'],
            escola=self.cleaned_data['escola']
        )
        usuario.save()
        print("Dados adicionais do usuário salvos com sucesso.")
    return user

def register(request):
    if request.method == 'POST':
        print("POST recebido")
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            form.save()
            return redirect('login')  # Certifique-se de que a URL 'login' está mapeada no seu urls.py
        else:
            print("Erros no formulário:", form.errors)  # Adiciona um print para exibir os erros

    else:
        form = RegisterForm()

    return render(request, 'login/register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')
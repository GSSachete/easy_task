from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

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

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para o login após registro
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

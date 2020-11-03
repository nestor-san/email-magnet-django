from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm

# Create your views here.


def index(request):
    return render(request, 'email_magnet/index.html')

def detail_search(request):
    return render(request, 'email_magnet/detail_search.html')

def brute_search(request):
    return render(request, 'email_magnet/brute_search.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('email_magnet:index')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})



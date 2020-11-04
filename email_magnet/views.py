from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, DetailSearchForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'email_magnet/index.html')


def detail_search(request):
    if request.method == 'POST':
        try:
            form = DetailSearchForm(request.POST)
            new_detail_search = form.save(commit=False)
            new_detail_search.user = request.user
            new_detail_search.save()
            #get_emails = new_detail_search.get_valid_email()
            #print(get_emails)
            return render(request, 'email_magnet/detail_search_done.html')
        except ValueError:
            return render(request, 'email_magnet/detail_search.html', {'form': form, 'error': 'There are errors in your data. Please, check and try again.'})

    else:
        form = DetailSearchForm()
    return render(request, 'email_magnet/detail_search.html', {'form': form})

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



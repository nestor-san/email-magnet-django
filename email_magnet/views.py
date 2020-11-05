from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, DetailSearchForm
from django.contrib.auth.decorators import login_required
from .models import DetailSearch
import csv

# Create your views here.

def index(request):
    return render(request, 'email_magnet/index.html')

@login_required
def detail_search(request):
    if request.method == 'POST':
        try:
            form = DetailSearchForm(request.POST)
            new_detail_search = form.save(commit=False)
            new_detail_search.user = request.user
            new_detail_search.save()
            return render(request, 'email_magnet/detail_search_done.html')
        except ValueError:
            return render(request, 'email_magnet/detail_search.html', {'form': form, 'error': 'There are errors in your data. Please, check and try again.'})

    else:
        form = DetailSearchForm()
    return render(request, 'email_magnet/detail_search.html', {'form': form})

@login_required
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

@login_required
def detailed_results(request):
    completed_searches = DetailSearch.objects.filter(valid_emails__isnull=False, user=request.user)
    pending_searches = DetailSearch.objects.filter(valid_emails=None, user=request.user)   
    return render(request, 'email_magnet/detailed_results.html', {'completed': completed_searches, 'pending': pending_searches})

@login_required
def detailed_search_detail(request, search_pk):
    search = get_object_or_404(DetailSearch, pk=search_pk, user=request.user)
    if request.method == 'POST':
        form = DetailSearchForm(request.POST, instance=search)
        try:
            form.save()
            search.possible_emails = None
            search.valid_emails = None
            form.save()
            return redirect('email_magnet:detailed_results')
        except ValueError:
            return render(request, 'email_magnet/detailed_search_view.html', {'search': search, 'form': form, 'error':'There was an issue with your data. Please, try again.'})
    else:
        form = DetailSearchForm(instance=search)
        return render(request, 'email_magnet/detailed_search_view.html', {'search': search, 'form': form})

@login_required
def delete_search(request, search_pk):
    search = get_object_or_404(DetailSearch, pk=search_pk, user=request.user)
    if request.method=='POST':
        search.delete()
        return redirect('email_magnet:detailed_results')

@login_required
def export_data(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="email_magnet_data.csv"'
        
        try:
            if request.POST['only_valid_emails'] and request.POST['pending_searches']:
                searches = DetailSearch.objects.filter(user=request.user).exclude(valid_emails='There are no valid emails')
        except: 
            try:
                if request.POST['only_valid_emails']:
                    searches = DetailSearch.objects.filter(user=request.user).exclude(valid_emails='There are no valid emails').filter(valid_emails__isnull=False)
            except:
                try:
                    if request.POST['pending_searches']:
                        searches = DetailSearch.objects.filter(user=request.user)
                except:
                    searches = DetailSearch.objects.filter(user=request.user).filter(valid_emails__isnull=False)

        writer = csv.writer(response)
        writer.writerow(['Domain name','First name','Middle name','Last name','Valid emails'])
        for search in searches:
            writer.writerow([search.domain,search.first_name,search.middle_name,search.last_name, search.valid_emails])
        return response  
    else:
        return render(request, 'email_magnet/export_data.html')

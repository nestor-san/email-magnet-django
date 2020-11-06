from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, DetailSearchForm
from django.contrib.auth.decorators import login_required
from .models import DetailSearch, BruteForceSearch
import csv
from validators import domain

# Create your views here.

def index(request):
    """
    This view loads the index page of the email magnet app
    """
    return render(request, 'email_magnet/index.html')

@login_required #decorator to require user login
def detail_search(request):
    """
    This view provides the functionality for the detailed search tool. 
    If the request is POST, it try to create a new detailed search in the database.
    If the data is valid, it creates the detailed search. If the data is invalid, it shows a message error.
    If the request is GET, this view loads the DetailSearchForm and the site for the user to fill all the data.
    """
    #check the request.method
    if request.method == 'POST':
        #Try to create the DetailSearch instance with DetailSearchForm data
        try:
            form = DetailSearchForm(request.POST)
            new_detail_search = form.save(commit=False)
            new_detail_search.user = request.user
            new_detail_search.save()
            #render a template with success result message
            return render(request, 'email_magnet/detail_search_done.html')

            #Generate error message if the data is invalid
        except ValueError:
            return render(request, 'email_magnet/detail_search.html', {'form': form, 'error': 'There are errors in your data. Please, check and try again.'})
    
    #if the request method is not POST, it loads the else statement. 
    # Expecting a GET request. 
    else:
        #Load the detailed search form.
        form = DetailSearchForm() 
        #Render the template with the form as context dictionary
        return render(request, 'email_magnet/detail_search.html', {'form': form})

@login_required #decorator to require user login
def brute_search(request):
    """
    This view loads the functionality for the Brute Search (Still under development). 
    If the request is POST, it validates the domain name provided by the user.
    If valid, a new instance of BruteForceSearch is created. If invalid, the user is returned to the prevoius
    page and wee a warning message.
    If the request is GET, this view loads the page with the form to provide the data for the new BruteForceSearch instance.
    """
    #Check the request method. If POST, load the if statement
    if request.method == 'POST':
        #create variable to store the domain name of the company provided by the user
        domain_name = request.POST['company_domain']

        # validate the domain name with validator domain. Validator return TRUE if valid domain name.
        if domain(domain_name):
            #create a variable to store the new BruteForceSearch instance
            brute_search = BruteForceSearch(domain=domain_name)
            #Save the BruteForceSearch instance
            brute_search.save()
            #render a template with success result message
            return render(request, 'email_magnet/brute_search_done.html')

        # validator return ValidationFailure if the domain ame is not valid. So it loads the else statement.  
        else:
            #the error message for invalid domain
            error = 'There is an error with your domain. Please, check it and try again. Note: Your domain should not include https:// nor www. Just write "yourdomain.com" or "guess.com" or "google.com" or "whatever.com".'
            #Render again Brute Search form with error message, so user can correct the data
            return render(request, 'email_magnet/brute_search.html', {'error': error})

    #If the request method is not POST, it loads ths else statement. Expecting a GET request.              
    else:
        return render(request, 'email_magnet/brute_search.html')

def sign_up(request):
    """
    This view loads the sign up page and process the user input. 
    If the request is POST, it try to create a new user or handle the error. 
    If the request is GET, it show the user RegisterForm.
    """
    #Check the request method. Load if statement if POST.
    if request.method == 'POST':
        #load the form for user registration
        form = RegisterForm(request.POST)
        #validate the form
        if form.is_valid():
            form.save() #save the form and create a new user
            username = form.cleaned_data.get('username') #load the username
            raw_password = form.cleaned_data.get('password1') #load the password
            user = authenticate(username=username, password=raw_password) #load an user with previous username and password
            login(request, user) #automatically authenticate the new user
            return redirect('email_magnet:index') #redirect he user to the index page

    #Load this else statement if the request is not POST. Expecting a GET request.
    else:
        #load the form for user registration in variable form
        form = RegisterForm()
        #return the sign up page with the Register form as context dictionary
        return render(request, 'registration/sign_up.html', {'form': form})

@login_required #decorator to require user login
def detailed_results(request):
    """
    This view loads the page for the user to see the results of the detailed search created.
    It shows the completed searches, that returna valid email or an error message.
    Apart, it shows the pending serches, these searches were created by the user but are still
    not being processed by the system, so valid email field is empty.
    """
    #Retrieve the data for the completed searches
    completed_searches = DetailSearch.objects.filter(valid_emails__isnull=False, user=request.user)
    #Retrieve the data for the pending searches
    pending_searches = DetailSearch.objects.filter(valid_emails=None, user=request.user)   
    #Render the template to show the data and load the previous retrieved data as two separate variables, to handle independently
    return render(request, 'email_magnet/detailed_results.html', {'completed': completed_searches, 'pending': pending_searches})
 
@login_required #decorator to require user login
def detailed_search_detail(request, search_pk):
    """
    This view load the details of a single detailed search. It retrieve a single search with the search.id and user,
    so it check the user is the owner of the search before loading. If any error, it loads 404 error.
    If the request is POST, it try to update the values of the search or handle the error. 
    If the request is GET, it loads the data of the search and provides a form to edit it.
    """
    #Get the single search data or raise a 404 error
    search = get_object_or_404(DetailSearch, pk=search_pk, user=request.user)
    #Check the request method. If POST, load the if statement
    if request.method == 'POST':
        #Load a variable with the request.POST form information
        form = DetailSearchForm(request.POST, instance=search)
        #try to save the data provided by the user
        try:
            form.save()
            #Restore to blank the possible emails field, so it will be recalculated.
            search.possible_emails = None
            #Restore to blank the valid emails field, so it will be recalculated.
            search.valid_emails = None
            #Save the changs
            form.save()
            #Redirect the user back to the detailed results page
            return redirect('email_magnet:detailed_results')
        #If the data provided by the user raise an error. Load the except:    
        except ValueError:
            #Render again the single search page and raise a warning about the data, so user can correct it.
            return render(request, 'email_magnet/detailed_search_view.html', {'search': search, 'form': form, 'error':'There was an issue with your data. Please, try again.'})
    
    #If the request method is not POST, load this else statement. Expecting a GET request.
    else:
        #Load the form to edit a single search
        form = DetailSearchForm(instance=search)
        #Return the single search page, with the instance of the search we're looking for loaded as search
        #and the form loaded as form.
        return render(request, 'email_magnet/detailed_search_view.html', {'search': search, 'form': form})

@login_required #decorator to require user login
def delete_search(request, search_pk):
    """
    This view provides a simple interface to delete a detailed search. For security, it check that the user
    that does the request is the same than the user who owns the detailed search. If any error, it raieses a
    404 error. 
    """
    #Load the search based in the parameters provided: id and user
    search = get_object_or_404(DetailSearch, pk=search_pk, user=request.user)
    #Check that the request method is POST
    if request.method=='POST':
        #Delete the single search
        search.delete()
        #Return the detailed results page
        return redirect('email_magnet:detailed_results')
    #Handle the exception of a GET request pointing to the delete URL
    else:
        #Return the detailed results page
        return redirect('email_magnet:detailed_results')

@login_required #decorator to require user login
def export_data(request):
    """
    This view loads a simple interface to export the user data searches. Once the data request
    is Done, it create a .csv file with the data provided. There are a couple of optional 
    parameters to customize the data export. 
    The functionality use try/except statements to handle HTML form checkboxes. It's not the
    most elegant solution, so it may be refactored in the next version.
    """
    #Check the request method. Load this for POST request. 
    if request.method == 'POST':
        #Define the Http Response as csv file
        response = HttpResponse(content_type='text/csv')
        #Make the csv file available for download and define the name of the file
        response['Content-Disposition'] = 'attachment; filename="email_magnet_data.csv"' #change this name if required
        #Customize the data based in two different options/parameters.
        #First this code checks if the user opted for "only valid emails" and "include pending searches"
        try:
            #Check the info of the request post. In case it contains "only valid emails" and "include pending searches"
            #load the searches accordingly
            if request.POST['only_valid_emails'] and request.POST['pending_searches']:
                #Get detailed searches of one user and exclude searches that didn't provide a valid email
                searches = DetailSearch.objects.filter(user=request.user).exclude(valid_emails='There are no valid emails')

        #If there is an error raised (because the POST request didn't contain any of the fields requested above). 
        except: 
            #This try statement try to load a search with "only valid emails" activated.           
            try:
                #Check the info of the request post. In case it contains "only valid emails", load the searches accordingly
                if request.POST['only_valid_emails']:
                    #Get detailed searches of one user, exclude emails which are not valid and filter only rows whose "valid emails" fields is not empty.
                    searches = DetailSearch.objects.filter(user=request.user).exclude(valid_emails='There are no valid emails').filter(valid_emails__isnull=False)
            #If there is an error raised (because the POST request didn't contain any of the fields requested above). Load this:
            except:                
                try:
                    #Check the info of the request post. In case it contains "include pending searches", load the searches accordingly.
                    if request.POST['pending_searches']:
                        #Get detailed searches of one user, including the pending ones.
                        searches = DetailSearch.objects.filter(user=request.user)
                #If it raises an error, this means the user didn't select any option.         
                except:
                    #Load searches of one user and filter when valid emails fiels is NULL. This way, it filter out the
                    # pending searches and show only finished searches (with valid emails or 'There are no valid emails' warning) 
                    searches = DetailSearch.objects.filter(user=request.user).filter(valid_emails__isnull=False)

        #Create the writer for the csv file
        writer = csv.writer(response)
        #Write the first row of the csv file with the header names
        writer.writerow(['Domain name','First name','Middle name','Last name','Valid emails'])
        #Run a for loop with all the searches
        for search in searches:
            #For any search, write a new row in the csv file with the info detailed in the header
            writer.writerow([search.domain,search.first_name,search.middle_name,search.last_name, search.valid_emails])
        #When all the info of the searches has been transfered to the csv, create a response as specified at the begining
        # of th view (A csv downloadable file)    
        return response  

    #If the request method is not POST, laod the else statement. Expecting a GET request.    
    else:
        #Render the page to set up the export of data.
        return render(request, 'email_magnet/export_data.html')

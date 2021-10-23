#-------------------------------------------------------------------------------------------------------------------------------
# Imports

from django.db.models.query import RawQuerySet
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm,LoginForm
from django.contrib.auth import authenticate, login
from survey_app.forms import CodeForm
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UsernameField
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
import string
import random
from django.core.exceptions import ValidationError
from axes.models import AccessAttempt
from json import dumps
from django.contrib.auth import authenticate
from django.urls import reverse

from .utils import send_email_login , send_email_register,send_warning_email
import time

#-------------------------------------------------------------------------------------------------------------------------------
# Otp generator function

def id_generator(size=6, chars=string.ascii_uppercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size))

# generating a random code with 6 characters and assigning it into a string using join method
#The join() method takes all items in an iterable and joins them into one string.
#https://www.w3schools.com/python/ref_string_join.asp

#-------------------------------------------------------------------------------------------------------------------------------
# Register view

def user_register(request): # to facilitate server client communication
    if request.user.is_authenticated:
        return redirect(reverse('home')) # if user is already logged in and tries to go to register page they will be redirected to home page
    if request.method == 'POST': # check if method is post
        form = UserRegisterForm(request.POST) # if true populating the form with post data
        if form.is_valid(): # checking if form is valid
            form.save() # if yes save the form

            #username = form.cleaned_data.get('username')
            
            messages.success(request, f'Your account has been created! You are now able to log in') # success message

            new_user = authenticate(request,username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            # authenticating the user
            #login(request, new_user)

            if new_user is not None: # checking if user and password combination exist in db
                request.session['pk'] = new_user.pk # setting user pk to a session 
                return redirect('register-verify-view') # going to r 
            else:
                messages.warning(request, f'Enter valid details!')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

#-------------------------------------------------------------------------------------------------------------------------------
# Register verify view

code_dict_r = {} #creating a dict to store otp
def user_register_verify_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    form = CodeForm(request.POST or None) # none makes the form loo empty during a get request
    pk = request.session.get('pk') # get primary from the current session

    global code_dict_r # calling the global var code_dict_r

    
    if pk:

        user = User.objects.get(pk=pk) # getting user from session pk

        if not request.POST: # checking if request is not post
            global code_r # declaring code r as global
            global code_time_r # declaring code_time_r as global
            code_r = id_generator() # generating the code
            code_dict_r[pk] = code_r # assigning the otp with pk as key
            print(code_dict_r)
            
            print(code_r)
            send_email_register(code_r,user.email,user) # sending email

            code_time_r = time.time() # storing the time after otp is generated
            
            
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if code_dict_r[request.session.get('pk')] == num and time.time() - code_time_r < 121: # sub current time from otp gen time, and checking if its less than 2 min
                login(request, user,backend='axes.backends.AxesBackend') # if true login
                #messages.success(request, f'You are logged in successfully') # send success msg
                del code_dict_r[request.session.get('pk')] # deleting the otp of the authenticated user
                return redirect('user_interests') # redirect to user interests page
            else:
                messages.warning(request, f'Enter valid details') # if error occurs send error msg
    return render(request,'users/register_verify.html',{'form':form}) # sending form to template

#-------------------------------------------------------------------------------------------------------------------------------
# Login view

counter_dict = {}
time_dict = {}
def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home')) # if user is authenticated and tries to go to the login page,they will be redirected to home page.
    
    global counter_dict # accessing the global var
    global time_dict # accessing the global var

    form = LoginForm() # storing the form in a var
    if request.method == 'POST': # checking if request is post
        username = request.POST.get('username') # get the username and store it in the var username
        password = request.POST.get('password') # get the password and store it in the var password

        try:
            match = User.objects.get(username=username) # check if username exist, if yes continue
        except User.DoesNotExist: # if doesnot exist not storing logs, redirecting again to login page and showing error msg
            # Unable to find a user, this is fine
            messages.warning(request,f'invalid data')
            print('anonymous user '+username)
            return redirect('login')
        
            
        user = authenticate(request, username=username, password=password) 

        #https://stackoverflow.com/questions/28249276/whats-the-difference-between-authenticate-and-login#:~:text=2%20Answers&text=To%20further%20clarify%2C%20authentication%20is,activities%20without%20repeated%20authentication%20checks.
        #https://django.readthedocs.io/en/1.3.X/topics/auth.html#:~:text=authenticate(),invalid%2C%20authenticate()%20returns%20None.

        if username not in counter_dict:
            counter_dict[username] = 0 # if the username is not in counterdict make it zero
            

        if user is not None:
            if username in time_dict:
                if time.time() - time_dict[username] >= 60: # sub current time from the five attempts failed time
                    counter_dict[username] = 0 # resetting the counter to 0
                    request.session['pk'] = user.pk
                    return redirect('login-verify-view')
            else:
                request.session['pk'] = user.pk
                return redirect('login-verify-view')

        else:
            # if login not successful
            if counter_dict[username] < 5: 
                counter_dict[username] += 1
                print(counter_dict)
            
            elif counter_dict[username] == 5:
                time_dict[username] = time.time()
                usr = User.objects.get(username__exact=username) # getting username from db
                # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#std:fieldlookup-exact
                #SQL equivalents: SELECT ... WHERE username = username;

                u_email = usr.email # extracting email
                send_warning_email(u_email) # sending warning email
                print('we are here')
            else:
                pass
      
            messages.warning(request, f'Enter valid details')


    return render(request, 'users/login.html', {'form':form,})

#-------------------------------------------------------------------------------------------------------------------------------
# Login verify view



code_dict_l = {}
def user_login_verify_view(request):
        
    if request.user.is_authenticated:
        return redirect(reverse('home'))
        
    

    form = CodeForm(request.POST or None) # None is returned if get request, else post request
    pk = request.session.get('pk') # getting session pk

    global code_dict_l
  

    
    if pk:
        user = User.objects.get(pk=pk)
        # code_l = None
       

        if not request.POST:
            global code_l
            global code_time_l
            code_l = id_generator()
            code_dict_l[pk] = code_l
            print(code_l)
            #send_email_login(code_l,user.email,user)
            code_time_l = time.time() # ifs the time since epoach
        if form.is_valid():
            num = form.cleaned_data.get('number')
            print(num)
            print(code_l)

            if code_dict_l[request.session.get('pk')] == num and time.time() - code_time_l < 121:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                #messages.success(request, f'You are logged in successfully')
                del code_dict_l[request.session.get('pk')]
                print(code_dict_l)
                return redirect('home')

            else:
                messages.warning(request, f'Enter valid otp!')
    else:
        return redirect(reverse('register'))

           
    return render(request,'users/login_verify.html',{'form':form,'code':code_l})

#-------------------------------------------------------------------------------------------------------------------------------
# Profile view

@login_required
def profile(request):
    print("we are here at update view")
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) # populating form with current data and post data
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            print("update successful")
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # we are redirecting for a get request, if we refresh

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

#-------------------------------------------------------------------------------------------------------------------------------
# Change password view 

@login_required
def change_password(request):
    if request.method == 'POST': # checking if request is post
        form = PasswordChangeForm(request.user, request.POST) # passing request.user  and populating form with the data
        if form.is_valid(): # checking if form is valid
            user = form.save() # if yes saving the form
            update_session_auth_hash(request, user)  # Important! Otherwise the user’s auth session will be invalidated and she/he will have to log in again.

            messages.success(request, 'Your password was successfully updated!') # sending a success msg
            return redirect('user-profile') # redirecting user to profile page
        else:
            messages.warning(request, 'Please correct the error below.') # if something goes wrong returning a error msg
    else:
        form = PasswordChangeForm(request.user) # if get request just show the form alone
    return render(request, 'users/change_password.html', {
        'form': form
    }) # rendering the form in html using change_password template

#https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html

#-------------------------------------------------------------------------------------------------------------------------------
# Delete user view

# class UserDeleteView(SuccessMessageMixin,DeleteView):
#     model = User
#     success_message = (f'Account deleted successfully')
#     success_url = reverse_lazy('register')

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super().delete(request, *args, **kwargs)

@login_required
def delete_user(request, username):
    user = User.objects.get(username__exact=username) # getting username from the request made
    profile = User.objects.filter(username=user.username) # filtering the user
    if request.method == 'POST': # if post
        profile.delete() # delete the user
        #messages.success(request,f'Account deleted successfully') # success msg
        return redirect('home') # redirecting to home

        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#std:fieldlookup-exact
        #SQL equivalents: SELECT ... WHERE username = username;

    
    return render(request, 'users/delete.html')

#-------------------------------------------------------------------------------------------------------------------------------
# Logout view

@login_required
def user_logout(request):
    time.sleep(2) # waiting for 2 sec
    logout(request) # using django.contrib.auth.logout(), It takes an HttpRequest object and has no return value
    messages.success(request,f'You are logged out successfully') # logout success msg
    return redirect('login') # redirect to login page

# https://www.kite.com/python/docs/django.contrib.auth.logout

#-------------------------------------------------------------------------------------------------------------------------------

# other links

#https://askubuntu.com/questions/431606/what-should-i-do-when-i-get-there-are-stopped-jobs-error



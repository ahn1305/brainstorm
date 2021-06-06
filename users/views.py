from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm,LoginForm
from django.contrib.auth import authenticate, login
from survey_app.forms import CodeForm
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
import string
import random

from .utils import send_email
import time


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, f'Your account has been created! You are now able to log in')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            #login(request, new_user)

            if new_user is not None:
                request.session['pk'] = new_user.pk
                return redirect('register-verify-view')
            else:
                messages.warning(request, f'Enter valid details!')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

code_dict_r = {} #creating a dict to store otp
def user_register_verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')

    
    if pk:

        user = User.objects.get(pk=pk)
        #code = user.code
        #{user.username}

        if not request.POST:
            global code_r
            global code_time_r
            code_r = id_generator()
            code_dict_r[pk] = code_r # assigning the otp with pk as key
            print(code_dict_r)
            
            print(code_r)

            code_time_r = time.time()
            
            #send_email(code_user,user.email)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if code_dict_r[request.session.get('pk')] == num and time.time() - code_time_r < 11:
                login(request, user)
                messages.success(request, f'You are logged in successfully')
                del code_dict_r[request.session.get('pk')] # deleting the otp of the authenticated user
                return redirect('user_interests')
            else:
                messages.warning(request, f'Enter valid otp!')
    return render(request,'users/register_verify.html',{'form':form})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['pk'] = user.pk
            return redirect('login-verify-view')
        else:
            messages.warning(request, f'Enter valid details!')

    return render(request, 'users/login.html', {'form':form})

code_dict_l = {}
def user_login_verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')

    global code_dict
    
    
    if pk:
        user = User.objects.get(pk=pk)
        #code_l = None
       

        if not request.POST:
            global code_l
            global code_time_l
            code_l = id_generator()
            code_dict_l[pk] = code_l
            print(code_dict_l)
            #send_email(code_user,user.email)
            print(code_l)
            code_time_l = time.time()
        if form.is_valid():
            num = form.cleaned_data.get('number')
            print(num)
            print(code_l)

            if code_dict_l[request.session.get('pk')] == num and time.time() - code_time_l < 11:
                login(request, user)
                messages.success(request, f'You are logged in successfully')
                del code_dict_l[request.session.get('pk')]
                return redirect('home')

            else:
                messages.warning(request, f'Enter valid otp!')

           
    return render(request,'users/login_verify.html',{'form':form})

@login_required
def profile(request):
    print("we are here at update view")
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user-profile')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('register')
    success_message = (f'Account deleted successfully')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

def user_logout(request):
    time.sleep(3)
    logout(request)
    messages.success(request,f'You are logged out successfully')
    return redirect('login')
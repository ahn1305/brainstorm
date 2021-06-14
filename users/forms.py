from django.contrib.auth import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        raise forms.ValidationError('This email address is already in use.')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',
    widget= forms.TextInput
                           (attrs={'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email')


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image','bio','website_url','instagram_url','facebook_url','twitter_url','github_url','linkedin_url']
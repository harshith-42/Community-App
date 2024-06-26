"""A model form is a class based representation of a form"""

from django.forms import ModelForm
from .models import Cohort, User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CohortForm(ModelForm):
    class Meta:
        model = Cohort
        fields = '__all__'
        exclude = ['host']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'bio', 'avatar']
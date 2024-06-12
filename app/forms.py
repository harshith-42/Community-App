"""A model form is a class based representation of a form"""

from django.forms import ModelForm
from .models import Cohort
from django.contrib.auth.models import User

class CohortForm(ModelForm):
    class Meta:
        model = Cohort
        fields = '__all__'
        exclude = ['host']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
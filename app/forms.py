"""A model form is a class based representation of a form"""

from django.forms import ModelForm
from .models import Cohort

class CohortForm(ModelForm):
    class Meta:
        model = Cohort
        fields = '__all__'
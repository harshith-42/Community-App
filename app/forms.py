from django.forms import ModelForm
from .models import Cohort

class CohortForm(ModelForm):
    class Meta:
        model = Cohort
        fields = '__all__'
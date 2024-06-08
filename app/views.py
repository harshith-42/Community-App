from django.shortcuts import render, redirect
from .models import Cohort
from .forms import CohortForm



def home(request):
    cohorts = Cohort.objects.all()
    context = {'cohorts': cohorts}
    return render(request, 'app/home.html', context)


def cohort(request, pk):
    cohort = Cohort.objects.get(id=pk)

    context = {'cohort': cohort}
    return render(request, 'app/cohort.html', context)

def createCohort(request):
    form = CohortForm()

    if request.method =='POST':
        form = CohortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form': form}
    return render(request, 'app/cohort_form.html', context)

def updateCohort(request, pk):
    cohort = Cohort.objects.get(id=pk)
    form = CohortForm(instance=cohort) # to pre fill form with the existing values
    
    if request.method == 'POST':
        form = CohortForm(request.POST, instance=cohort)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'app/cohort_form.html', context)

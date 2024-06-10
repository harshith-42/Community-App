from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Cohort, Topic
from .forms import CohortForm


def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')                     # To not allow loggin in user to login again

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password may not exist')

    context = {'page':page}
    return render(request, 'app/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'app/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    cohorts = Cohort.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    cohort_count = cohorts.count()

    context = {'cohorts': cohorts, 'topics': topics, 'cohort_count':cohort_count}
    return render(request, 'app/home.html', context)


def cohort(request, pk):
    cohort = Cohort.objects.get(id=pk)
    cohort_messages = cohort.message_set.all() # Get all the messages related to this cohort
    context = {'cohort': cohort, 'cohort_messages':cohort_messages}
    return render(request, 'app/cohort.html', context)

@login_required(login_url='login')
def createCohort(request):
    form = CohortForm()

    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'app/cohort_form.html', context)


@login_required(login_url='login')
def updateCohort(request, pk):
    cohort = Cohort.objects.get(id=pk)
    # to pre fill form with the existing values
    form = CohortForm(instance=cohort)

    if request.user != cohort.host:
        return HttpResponse('You are not the host of this cohort')

    if request.method == 'POST':
        form = CohortForm(request.POST, instance=cohort)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'app/cohort_form.html', context)

@login_required(login_url='login')
def deleteCohort(request, pk):
    cohort = Cohort.objects.get(id=pk)

    if request.user != cohort.host:
        return HttpResponse('You are not the host of this cohort')

    if request.method == 'POST':
        cohort.delete()
        return redirect('home')
    return render(request, 'app/delete.html', {'obj': cohort})

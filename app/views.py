from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Cohort, Topic, Message, User, Follow
from .forms import CohortForm, UserForm, CustomUserCreationForm


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
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'app/login_register.html', {'form': form})


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

@login_required(login_url='login')
def cohort(request, pk):
    cohort = Cohort.objects.get(id=pk)
    cohort_messages = cohort.message_set.all() # Get all the messages related to this cohort
    participants = cohort.participants.all()
    if request.method =='POST':
        message = Message.objects.create(
            user = request.user,
            cohort = cohort,
            body = request.POST.get('body')
        )
        cohort.participants.add(request.user) # To add user to participants list
        return redirect('cohort', pk=cohort.id)
    context = {'cohort': cohort, 'cohort_messages':cohort_messages, 'participants':participants}
    return render(request, 'app/cohort.html', context)



@login_required(login_url='login')
def createCohort(request):
    form = CohortForm()

    if request.method == 'POST':
        form = CohortForm(request.POST)
        if form.is_valid():
            cohort = form.save(commit=False)
            cohort.host = request.user
            cohort.save()
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'app/cohort_form.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = get_object_or_404(User, id=pk)
    cohorts = user.cohort_set.all()
    topics = Topic.objects.all()
    is_following = Follow.objects.filter(from_user=request.user, to_user=user).exists() if request.user.is_authenticated else False
    context = {'user': user, 'cohorts': cohorts, 'topics': topics, 'is_following': is_following}
    return render(request, 'app/profile.html', context)


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


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not the owner of this message')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'app/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'app/update_user.html', {'form': form})


def toggle_follow(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        to_user = get_object_or_404(User, id=user_id)

        if action == 'follow':
            Follow.objects.get_or_create(from_user=request.user, to_user=to_user)
        elif action == 'unfollow':
            Follow.objects.filter(from_user=request.user, to_user=to_user).delete()

        return redirect('user-profile', pk=to_user.id)  # Use 'pk' here
    return redirect('home')

def followers_list(request, pk):
    user = get_object_or_404(User, id=pk)
    followers = Follow.objects.filter(to_user=user).select_related('from_user')
    context = {'user': user, 'followers': followers}
    return render(request, 'app/followers_list.html', context)

def following_list(request, pk):
    user = get_object_or_404(User, id=pk)
    following = Follow.objects.filter(from_user=user).select_related('to_user')
    context = {'user': user, 'following': following}
    return render(request, 'app/following_list.html', context)

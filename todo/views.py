from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

from .forms import SignUpForm,SignInForm
from .models import Task


def index(request):
    signup_form = SignUpForm()
    login_form = SignInForm()
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=email, email=email, password=password, first_name=name)
            messages.success(request, 'User created successfully!')
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'index.html', {'signup_form': form})


def signin_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Authenticate using username instead of email
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('todolist')  # Replace 'todolist' with the appropriate URL name for your todolist page
        else:
            messages.error(request, 'Invalid email or password')
    return redirect('index')  # Replace 'index' with the appropriate URL name for your index page


def task_view(request):
    return render(request, 'todo.html')


@login_required
def todolist_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todolist.html', {'tasks': tasks})


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Mark the task as completed (update the completed field to True)
    if not task.completed:
        task.completed = True
    else:
        task.completed = False
    task.save()
    return redirect('todolist')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Delete the task
    task.delete()
    return redirect('todolist')

def completed_list_view(request):
    tasks = Task.objects.filter(user=request.user,completed=True)
    return render(request, 'completed_list.html', {'tasks': tasks})

def logout_view(request):
    logout(request)
    return redirect('index')


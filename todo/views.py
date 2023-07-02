from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

from .forms import SignUpForm,SignInForm
from .models import Task
from .models import Theme

def index(request):
    signup_form = SignUpForm()
    login_form = SignInForm()
    return render(request, 'index.html', {'signup_form': signup_form, 'login_form': login_form})


from .models import Theme


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)

            # Create a Theme object for the user with the default scheme
            theme = Theme.objects.create(user=user)

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


def task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    theme = Theme.objects.get(user= request.user)

    context ={
        'task': task,
        'theme': theme,
    }
    return render(request, 'todo.html', context)



def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.name = request.POST.get('inputTask')
        task.category = request.POST.get('inputCategory')
        task.priority = request.POST.get('inputPriority')
        task.date = request.POST.get('date')
        task.completed = request.POST.get('status') == 'on'
        task.save()
        return redirect('todolist')
    return render(request, 'todo.html', {'task': task})





@login_required
def todolist_view(request):
    tasks = Task.objects.filter(user=request.user)
    theme = Theme.objects.filter(user=request.user).first()
    context = {
        'tasks': tasks,
        'theme': theme,
    }
    return render(request, 'todolist.html', context)


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Mark the task as completed (update the completed field to True)
    if not task.completed:
        task.completed = True
        task.save()
        return redirect('todolist')
    else:
        task.completed = False
        task.save()
        return redirect('completed')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Delete the task
    task.delete()
    return redirect('todolist')

def completed_list_view(request):
    tasks = Task.objects.filter(user=request.user,completed=True)
    theme = Theme.objects.get(user=request.user)
    context = {
        'tasks': tasks,
        'theme': theme,
    }
    return render(request, 'completed_list.html', context)


def theme_update(request):
    theme = Theme.objects.get(user=request.user)
    if request.method == "POST":
        theme.scheme = request.POST.get('inputTheme')
        theme.save()
        return redirect('todolist')


def task_create(request):
    if request.method == "POST":
        name = request.POST.get('inputTask')
        category = request.POST.get('inputCategory')
        priority = request.POST.get('inputPriority')
        date = request.POST.get('date')
        status = request.POST.get('status') == 'on'
        task = Task.objects.create(user=request.user, name=name, category=category, priority=priority, date=date, completed=status)
        task.save()
        return redirect('todolist')

def task_new(request):
    theme = Theme.objects.get(user=request.user)
    return render(request,'create.html', {'theme': theme})

def logout_view(request):
    logout(request)
    return redirect('index')


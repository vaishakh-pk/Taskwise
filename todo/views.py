from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from todo_list import settings
from .forms import SignUpForm, SignInForm
from .models import Task


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

            if User.objects.filter(first_name=name).exists():
                messages.success(request, 'Huff ,Username already exist')
                return redirect("signin")
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Come On, Email was already Taken !')
                return redirect("signin")
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
                user.save()
                mydict = {'username': name}
                html_template = 'registered_mail.html'
                html_message = render_to_string(html_template, context=mydict)
                subject = 'Welcome to TaskWise'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = EmailMessage(subject, html_message,
                                       email_from, recipient_list)
                message.content_subtype = 'html'
                message.send()

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
            theme = Theme.objects.get(user=request.user)
            theme.category = 'All'
            theme.save()
            return redirect('todolist')  # Replace 'todolist' with the appropriate URL name for your todolist page
        else:
            messages.error(request, 'Invalid email or password')
    return redirect('index')  # Replace 'index' with the appropriate URL name for your index page


def task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    theme = Theme.objects.get(user=request.user)

    context = {
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
        task.notification = False
        task.save()
        return redirect('todolist')
    return render(request, 'todo.html', {'task': task})


@login_required
def todolist_view(request):
    theme = Theme.objects.filter(user=request.user).first()
    if theme.category == 'All':
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = Task.objects.filter(user=request.user, category=theme.category)
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
    tasks = Task.objects.filter(user=request.user, completed=True)
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


def category_update(request):
    theme = Theme.objects.get(user=request.user)
    if request.method == "POST":
        theme.category = request.POST.get('inputCategory')
        theme.save()
        return redirect('todolist')


def task_create(request):
    if request.method == "POST":
        name = request.POST.get('inputTask')
        category = request.POST.get('inputCategory')
        priority = request.POST.get('inputPriority')
        date = request.POST.get('date')
        status = request.POST.get('status') == 'on'
        task = Task.objects.create(user=request.user, name=name, category=category, priority=priority, date=date,
                                   completed=status)
        task.save()
        task_date = datetime.strptime(date, '%Y-%m-%dT%H:%M').date()
        if task_date == datetime.now().date():
            print("Sending email-notification..")
            mydict = {
                'username': task.user.first_name,
                'task': task.name,
                'time': datetime.strptime(date, '%Y-%m-%dT%H:%M').time()
            }
            html_message = render_to_string('email-notification.html', mydict)
            subject = 'TaskWise reminder -' + task.name
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [task.user]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            task.notification = True
            task.save()
            print("Email sent successfully")
            return redirect('todolist')


def task_new(request):
    theme = Theme.objects.get(user=request.user)
    return render(request, 'create.html', {'theme': theme})


def logout_view(request):
    logout(request)
    return redirect('index')

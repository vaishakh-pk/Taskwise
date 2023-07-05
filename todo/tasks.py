# tasks.py

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task


@shared_task
def send_task_notifications():
    current_date = timezone.now().date()
    tasks = Task.objects.filter(date__date=current_date)
    admin = settings.EMAIL_HOST_USER
    for task in tasks:
        # Send email notification
        subject = f"Task Reminder: {task.name}"
        message = f"Hi {task.user.username},\n\nThis is a reminder for your task: {task.name}"
        send_mail(subject, message, admin, [task.user.email])

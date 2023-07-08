from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_list.settings')
django.setup()

from todo.models import Task


def notifty():
    tasks = Task.objects.filter(date__date=timezone.now().date())
    print("mail-service running...")
    for task in tasks:
        if not task.notification and not task.completed:
            print(task)
            mydict = {
                'username': task.user.first_name,
                'task': task.name,
                'time': task.date.time()
            }
            html_template = 'email-notification.html'
            html_message = render_to_string(html_template, mydict)
            subject = 'TaskWise reminder -' + task.name
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [task.user]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            task.notification = True
            task.save()


# ----------------------- AUTO SEND MESSAGE AT 00:00-----------------------------#

import datetime
import time

current_time = datetime.datetime.now().time()

newday = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time(0, 0))
time_remaining = (newday - datetime.datetime.now()).total_seconds()

while True:
    notifty()
    time.sleep(time_remaining)







from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Task
from django.conf import settings
import datetime


@receiver(post_save, sender=Task)
def send_task_notification(sender, instance, created, **kwargs):
    if created:
        today = datetime.date.today()

        if instance.date.date() == today:
            subject = 'Task Reminder: {}'.format(instance.name)
            message = render_to_string('task/email/notification_email.html', {'task': instance})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)

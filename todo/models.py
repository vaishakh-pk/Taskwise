from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High priority', 'High priority'),
        ('Medium priority', 'Medium priority'),
        ('Low priority', 'Low priority'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # New field for checkbox

    def __str__(self):
        return self.name

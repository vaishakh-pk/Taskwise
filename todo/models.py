from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [
    ('None', 'None'), ('Personal', 'Personal'), ('Health', 'Health'), ('Household', 'Household'), ('Work', 'Work'),
    ('Hobby', 'Hobby')
]


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High priority', 'High priority'),
        ('Medium priority', 'Medium priority'),
        ('Low priority', 'Low priority'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)  # New field for checkbox

    def __str__(self):
        return self.name


class Theme(models.Model):
    THEME_CHOICES = [
        ('DEFAULT', 'DEFAULT'),
        ('OCEAN', 'OCEAN'),
        ('FOREST', 'FOREST'),
        ('LIGHT', 'LIGHT'),
        ('DARK', 'DARK')
    ]

    STYLE_1 = {
        'DEFAULT': 'background: linear-gradient(to right, #fd8c76, #fa7896);',
        'OCEAN': 'background: linear-gradient(to right, #5ba7ff, #7567ff);',
        'FOREST': 'background: linear-gradient(to right, #57bb45, #4cb95d);',
        'LIGHT': 'background: linear - gradient(to right,  # b0b0b0, #949393);',
        'DARK': 'background: linear-gradient(to right, #2d2d2d, #000000);'
    }

    STYLE_2 = {
        'DEFAULT': 'background: linear-gradient(to right, #fcb0a2, #ff9baf);',
        'OCEAN': 'background: linear-gradient(to right, #76b5fd, #8578fa);',
        'FOREST': 'background: linear-gradient(to right, #88ff73, #76ff8c);',
        'LIGHT': 'background: linear-gradient(to right, #eaeaea, #d9d8d8);',
        'DARK': 'background: linear-gradient(to right, #939393, #484848);'
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheme = models.CharField(max_length=80, choices=THEME_CHOICES, default='DEFAULT')
    category = models.CharField(max_length=20, default='All')

    def __str__(self):
        return self.scheme

    @property
    def style1(self):
        return self.STYLE_1.get(self.scheme, self.STYLE_1['DEFAULT'])

    @property
    def style2(self):
        return self.STYLE_2.get(self.scheme, self.STYLE_2['DEFAULT'])

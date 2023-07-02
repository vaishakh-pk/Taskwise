from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('todolist/', views.todolist_view, name='todolist'),
    path('task/<int:task_id>/', views.task_view, name="task"),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('completed', views.completed_list_view, name="completed"),
    path('logout/', views.logout_view, name='logout'),
    path('task/update/<int:task_id>/', views.task_update, name='task_update'),
    path('theme_update/', views.theme_update, name='theme_update'),
    path('create/', views.task_new, name='task_new'),
    path('creating/', views.task_create, name='task_create'),

    # ...
    # Add other URL patterns as needed
]

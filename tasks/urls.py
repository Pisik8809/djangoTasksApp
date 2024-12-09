from django.urls import path
from . import views
from django.contrib import admin
from app.views import home

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('<int:task_id>/complete/', views.task_complete, name='task_complete'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Стартова сторінка
]

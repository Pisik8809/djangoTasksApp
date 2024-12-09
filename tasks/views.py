from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

# Список задач
@login_required
def task_list(request):
    tasks = Task.objects.filter(assignee=request.user)  # Відображати лише задачі користувача
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Створення задачі (з перевіркою прав)
@login_required
@permission_required('tasks.add_task', raise_exception=True)
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignee_id = request.POST.get('assignee')
        assignee = get_object_or_404(User, id=assignee_id)
        Task.objects.create(
            title=title,
            description=description,
            creator=request.user,
            assignee=assignee
        )
        return redirect('tasks:task_list')
    users = User.objects.filter(profile__role__name='Employee')  # Призначати задачі лише співробітникам
    return render(request, 'tasks/task_create.html', {'users': users})

# Деталі задачі
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

# Редагування задачі
@login_required
@permission_required('tasks.change_task', raise_exception=True)
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('tasks:task_detail', task_id=task.id)
    return render(request, 'tasks/task_edit.html', {'task': task})

# Завершення задачі
@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, assignee=request.user)
    task.completed = True
    task.save()
    return redirect('tasks:task_list')

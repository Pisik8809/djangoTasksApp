from django.contrib.auth.models import AbstractUser, User, Permission
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Модель для задач
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Модель ролі
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

# Додатковий профіль користувача
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

# Сигнал для обробки зміни ролі користувача
@receiver(pre_save, sender=UserProfile)
def check_role_change(sender, instance, **kwargs):
    
    # Перевіряє, чи змінилася роль, і якщо так, очищає старі права.
  
    if instance.pk:  
        previous = UserProfile.objects.get(pk=instance.pk)
        if previous.role != instance.role:
            # Якщо роль змінилася, очищаємо старі права
            instance.user.user_permissions.clear()

# Сигнал для автоматичного призначення прав на основі ролі
@receiver(post_save, sender=UserProfile)
def assign_permissions(sender, instance, created, **kwargs):
    
    #Призначає права користувачу на основі його ролі.
    
    if instance.role:
        # Призначити права з ролі
        instance.user.user_permissions.set(instance.role.permissions.all())

# Сигнал для оновлення прав користувачів при зміні прав у ролі
@receiver(post_save, sender=Role)
def update_user_permissions_on_role_change(sender, instance, **kwargs):
    
    #Оновлює права всіх користувачів, які мають змінену роль.
    # Знайти всі профілі, пов'язані з цією роллю
    for profile in UserProfile.objects.filter(role=instance):
        # Оновити права користувача
        profile.user.user_permissions.set(instance.permissions.all())

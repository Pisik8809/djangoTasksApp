from django.contrib.auth.models import AbstractUser, User, Permission
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# ������ ��� �����
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

# ������ ���
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

# ���������� ������� �����������
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

# ������ ��� ������� ���� ��� �����������
@receiver(pre_save, sender=UserProfile)
def check_role_change(sender, instance, **kwargs):
    
    # ��������, �� �������� ����, � ���� ���, ����� ���� �����.
  
    if instance.pk:  
        previous = UserProfile.objects.get(pk=instance.pk)
        if previous.role != instance.role:
            # ���� ���� ��������, ������� ���� �����
            instance.user.user_permissions.clear()

# ������ ��� ������������� ����������� ���� �� ����� ���
@receiver(post_save, sender=UserProfile)
def assign_permissions(sender, instance, created, **kwargs):
    
    #�������� ����� ����������� �� ����� ���� ���.
    
    if instance.role:
        # ���������� ����� � ���
        instance.user.user_permissions.set(instance.role.permissions.all())

# ������ ��� ��������� ���� ������������ ��� ��� ���� � ���
@receiver(post_save, sender=Role)
def update_user_permissions_on_role_change(sender, instance, **kwargs):
    
    #������� ����� ��� ������������, �� ����� ������ ����.
    # ������ �� ������, ���'���� � ���� �����
    for profile in UserProfile.objects.filter(role=instance):
        # ������� ����� �����������
        profile.user.user_permissions.set(instance.permissions.all())

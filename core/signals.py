from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Task, AuditLog
from core.middleware import CurrentUserMiddleware 
from django.db.models.signals import post_save

@receiver(post_save, sender=Project)
def log_project_changes(sender, instance, created, **kwargs):
    user = CurrentUserMiddleware.get_current_user() 

    action = "created" if created else "updated"
    AuditLog.objects.create(
        user=user, 
        tenant=instance.tenant,
        action=f"Project {action}",
        details=f"Project '{instance.name}' by {user.username if user else 'Unknown'}",
    )

@receiver(post_save, sender=Task)
def log_task_changes(sender, instance, created, **kwargs):
    user = CurrentUserMiddleware.get_current_user() 

    action = "created" if created else "updated"
    AuditLog.objects.create(
        user=user,  
        tenant=instance.tenant,
        action=f"Task {action}",
        details=f"Task '{instance.title}' by {user.username if user else 'Unknown'}",
    )

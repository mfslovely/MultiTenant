from django.contrib import admin
from .models import Tenant, CustomUser, Project, Task, AuditLog

admin.site.register(Tenant)
admin.site.register(CustomUser)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(AuditLog)
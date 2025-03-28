from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework import viewsets, permissions
from .permissions import IsTenantAdminOrManager
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Tenant, CustomUser,AuditLog
from core.middleware import CurrentUserMiddleware



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsTenantAdminOrManager]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        project = serializer.save(tenant=self.request.user.tenant)
        user = CurrentUserMiddleware.get_current_user()  
        # user = self.request.user 

        AuditLog.objects.create(
            user=user,  
            tenant=project.tenant,
            action="Project created",
            details=f"Project '{project.name}' created by {user.username}",
        )




class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        user = CurrentUserMiddleware.get_current_user()  
        task = serializer.save(tenant=self.request.user.tenant) 

        AuditLog.objects.create(
            user=self.request.user,  
            tenant=task.tenant,
            action="Task created",
            details=f"Task '{task.title}' created by {self.request.user.username}",
        )



@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_tenant(request):
    tenant_name = request.data.get('name')
    admin_username = request.data.get('admin_username')
    admin_password = request.data.get('admin_password')

    if Tenant.objects.filter(name=tenant_name).exists():
        return Response({"error": "Tenant already exists"}, status=status.HTTP_400_BAD_REQUEST)

    
    tenant = Tenant.objects.create(name=tenant_name)

    user = CustomUser.objects.create(
        username=admin_username,
        password=make_password(admin_password),
        role='tenant_admin',
        tenant=tenant
    )

    return Response({"message": "Tenant created", "tenant_id": tenant.id, "admin_id": user.id})

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def create_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", "user")

    tenant = request.user.tenant  

    new_user = CustomUser.objects.create_user(
        username=username,
        password=password,
        role=role,
        tenant=tenant
    )

    return Response({"message": "User created", "user_id": new_user.id})



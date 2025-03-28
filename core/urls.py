from django.urls import path
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, MyTokenObtainPairView,create_tenant,create_user

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-tenant/', create_tenant, name='create-tenant'),
    path('create-user/',create_user,name = 'create-user')
]

urlpatterns += router.urls



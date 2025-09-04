from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем router для ViewSets
router = DefaultRouter()
router.register(r'permissions', views.PermissionViewSet, basename='permission')
router.register(r'common_permissions', views.CommonPermissionsViewSet, basename='common_permission')

urlpatterns = [
    # Маршруты для ViewSets
    path('', include(router.urls)),

    # Маршруты для APIView
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
]
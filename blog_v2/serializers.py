from rest_framework import serializers
from .models import Role, Permission, CommonPermission
from django.contrib.auth import get_user_model

User = get_user_model()


# добавил 2 в имя модели так как схема ругается на совпадение в версиях
class Post2Serializer(serializers.Serializer):
    """Сериализатор для описания поста"""
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=600)


class PermissionSerializer(serializers.ModelSerializer):
    """Сериализатор для предоставления отдельных полномочий конкретному пользователю"""
    user_to_access_detail = serializers.CharField(source='user_to_access', read_only=True)
    element_detail = serializers.CharField(source='element', read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class CommonPermissionSerializer(serializers.ModelSerializer):
    """Сериализатор для общих разрешений ролей"""

    role_detail = serializers.CharField(source='role', read_only=True)

    class Meta:
        model = CommonPermission
        fields = '__all__'

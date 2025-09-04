from rest_framework import permissions
from .models import Permission, Post, CommonPermission
from rest_framework.exceptions import NotAuthenticated


class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            raise NotAuthenticated('Требуется аутентификация')

        # Проверяем правила доступа для роли пользователя
        try:
            common_rule = CommonPermission.objects.get(role=user.role)
        except (Post.DoesNotExist, Permission.DoesNotExist):
            return False

        # Проверяем права в зависимости от метода
        if request.method == 'GET':
            return common_rule.read_all_permission
        elif request.method == 'POST':
            return common_rule.create_permission
        elif request.method in ['PUT', 'PATCH']:
            return common_rule.update_all_permission
        elif request.method == 'DELETE':
            return common_rule.delete_all_permission

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            raise NotAuthenticated('Требуется аутентификация')

        element = obj

        try:
            rule = Permission.objects.get(user_to_access=user, element=element)
        except (Post.DoesNotExist, Permission.DoesNotExist):
            return False
        try:
            common_rule = CommonPermission.objects.get(role=user.role)
        except (Post.DoesNotExist, CommonPermission.DoesNotExist):
            return False

        # Проверяем права на конкретный объект
        if request.method == 'GET':
            if rule.read_permission or common_rule.read_all_permission:
                return True
            elif hasattr(obj, 'author'):
                return obj.author == user

        elif request.method in ['PUT', 'PATCH']:
            if rule.update_permission or common_rule.update_all_permission:
                return True
            elif hasattr(obj, 'author'):
                return obj.author == user

        elif request.method == 'DELETE':
            if rule.delete_permission or common_rule.delete_all_permission:
                return True
            elif hasattr(obj, 'author'):
                return obj.author == user

        return False

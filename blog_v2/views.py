from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Post, Permission, CommonPermission
from .serializers import PermissionSerializer, Post2Serializer, CommonPermissionSerializer
from .permissions import RoleBasedPermission

User = get_user_model()

tags = ["blog_v2"]


@extend_schema_view(
    list=extend_schema(tags=["Permissions"]),
    create=extend_schema(tags=["Permissions"]),
    retrieve=extend_schema(tags=["Permissions"]),
    update=extend_schema(tags=["Permissions"]),
    partial_update=extend_schema(tags=["Permissions"]),
    destroy=extend_schema(tags=["Permissions"])
)
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
    business_element = 'access_rules'


@extend_schema_view(
    list=extend_schema(tags=["CommonPermissions"]),
    create=extend_schema(tags=["CommonPermissions"]),
    retrieve=extend_schema(tags=["CommonPermissions"]),
    update=extend_schema(tags=["CommonPermissions"]),
    partial_update=extend_schema(tags=["CommonPermissions"]),
    destroy=extend_schema(tags=["CommonPermissions"])
)
class CommonPermissionsViewSet(viewsets.ModelViewSet):
    queryset = CommonPermission.objects.all()
    serializer_class = [CommonPermissionSerializer]
    permission_classes = [IsAdminUser]
    business_element = 'common_access_rules'


class PostListView(APIView):
    element = Post.objects.all()  # элемент(ы) для проверки прав
    serializer_class = Post2Serializer
    permission_classes = [RoleBasedPermission]

    @extend_schema(
        summary="Retrieve all Posts from blog_2",
        description="""
                    This endpoint allows to retrieve all posts for every consumer.
                """,
        tags=tags,
    )
    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create new post in blog_v2",
        description="""
                    This endpoint allows a authenticated user to add new post.
                """,
        tags=tags,
    )
    def post(self, request):
        """
        Создание нового поста
        Права проверяются автоматически через RoleBasedPermission
        """
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                post = serializer.save(author=request.user)
                response_serializer = self.serializer_class(post)
                return Response(
                    response_serializer.data,
                    status=201
                )
            else:
                return Response(
                    {'error': 'Неверные данные', 'details': serializer.errors},
                    status=400
                )

        except Exception as e:
            return Response(
                {'error': 'Ошибка сервера при создании поста'},
                status=500
            )


class PostDetailView(APIView):
    serializer_class = Post2Serializer
    permission_classes = [RoleBasedPermission]

    @extend_schema(
        summary="Retrieve Post from blog_v2",
        description="""
                    This endpoint allows an authenticated user to get detail information about the post.
                """,
        tags=tags,
    )
    def get(self, request, pk):
        try:
            post = get_object_or_404(Post, pk=pk)

            # Проверка прав на конкретный объект
            if not self.check_object_permissions(request, post):
                return Response(
                    {'error': 'Доступ к этому посту запрещен'},
                    status=403
                )

            serializer = self.serializer_class(post)
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'},
                status=404
            )
        except Exception as e:
            return Response(
                {'error': 'Ошибка сервера'},
                status=500
            )

    @extend_schema(
        summary="Edit Post",
        description="""
                    This endpoint allows a owner to edit his post or a editor.
                """,
        tags=tags,
    )
    def put(self, request, pk):
        """
        Обновление поста
        """
        try:
            post = get_object_or_404(Post, pk=pk)

            # Проверка прав на обновление конкретного объекта
            if not self.check_object_permissions(request, post):
                return Response(
                    {'error': 'Нет прав на обновление этого поста'},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = self.serializer_class(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Неверные данные', 'details': serializer.errors},
                    status=400
                )

        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'},
                status=404
            )
        except Exception as e:
            return Response(
                {'error': 'Ошибка сервера при обновлении поста'},
                status=500
            )

    @extend_schema(
        summary="Delete Post from blog_v2",
        description="""
                    This endpoint allows a owner or controller to delete post.
                """,
        tags=tags,
    )
    def delete(self, request, pk):
        """
        Удаление поста
        """
        try:
            post = get_object_or_404(Post, pk=pk)

            # Проверка прав на удаление конкретного объекта
            if not self.check_object_permissions(request, post):
                return Response(
                    {'error': 'Нет прав на удаление этого поста'},
                    status=403
                )

            post.delete()
            return Response(
                {'message': 'Пост успешно удален'},
                status=204
            )

        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Ошибка сервера при удалении поста'},
                status=500
            )

    def check_object_permissions(self, request, obj):
        """
        Кастомная проверка прав для объекта
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                return False
        return True


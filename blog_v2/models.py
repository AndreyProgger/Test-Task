from django.db import models
from django.utils import timezone
from django.conf import settings

from accounts.models import Role


class Post(models.Model):
    """
    Представляет объект поста в блоге

    Атрибуты:
        title (str): Заголовок поста
        author (ForeignKey): Пользователь являющейся автором поста
        body (str): Тело поста
        publish (DateTimeField): Время публикации поста
        created (DateTimeField): Время создания поста в БД
        updated (DateTimeField): Время последнего обновления поста
    """
    title = models.CharField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='blog_v2_posts')

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self) -> str:
        return self.title


class Permission(models.Model):
    """
    Представляет разрешения конкретного пользователя к конкретному объекту
        Атрибуты:
        user_to_access (ForeignKey): Пользователь, которому нужно изменить права на объект
        element (ForeignKey): Объект(пост в блоге), на который нужно изменить разрешение
        read_permission (BooleanField): Разрешение на чтение конкретного объекта
        update_permission (BooleanField): Разрешение на обновление конкретного объекта
        delete_permission (BooleanField): Разрешение на удаление конкретного объекта
        created (DateTimeField): Время создания разрешения в БД
        updated (DateTimeField): Время последнего обновления разрешения

    """
    user_to_access = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_rules')
    element = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='single_rules')

    read_permission = models.BooleanField(default=True)
    update_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Обеспечиваем уникальность конкретного разрешения
        unique_together = ['user_to_access', 'element']

    def __str__(self) -> str:  # Удобочитаемый формат вывода
        return f"{self.user_to_access.name} - {self.element.title}"


class CommonPermission(models.Model):
    """
    Представляет разрешения роли ко всем объектам
        Атрибуты:
        role (ForeignKey): Роль, которая имеет определенные разрешения
        read_all_permission (BooleanField): Разрешение на чтение всех объектов
        update_all_permission (BooleanField): Разрешение на обновление всех объектов
        delete_all_permission (BooleanField): Разрешение на удаление всех объектов
        created (DateTimeField): Время создания разрешения в БД
        updated (DateTimeField): Время последнего обновления разрешения
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='access_rules')

    read_all_permission = models.BooleanField(default=True)
    create_permission = models.BooleanField(default=True)
    update_all_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # Удобочитаемый формат вывода
        return (f"{self.role.name}: read_all_permission{self.read_all_permission},"
                f" create_permission{self.create_permission}, update_all_permission{self.update_all_permission},"
                f"delete_all_permission{self.delete_all_permission},")

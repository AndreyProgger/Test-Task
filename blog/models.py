from django.db import models
from django.utils import timezone
from django.conf import settings


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
                               related_name='blog_posts')

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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.managers import CustomUserManager


class Role(models.Model):
    """Представляет роль и полномочия пользователя в системе
        Атрибуты:
        name (str): Название роли
        description (str): Описание полномочий для каждой роли (опционально)
        created_at (DateTimeField): Время создания роли в БД"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'roles'

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser):
    """
    Представляет кастомную модель пользователя удовлетворяющую ТЗ

    Атрибуты:
        first_name (str): Имя пользователя
        last_name (str): Фамилия пользователя
        email (str): Тело поста
        patronymic (str): Отчество пользователя(опционально)
        role (ForeignKey): Роль пользователя в системе
        is_staff (BooleanField): Флаг проверяющий является ли пользователь админом
        is_active (BooleanField): Флаг проверяющий является ли пользователь активным
    """
    first_name = models.CharField(verbose_name="First name", max_length=25)
    last_name = models.CharField(verbose_name="Last name", max_length=25)
    email = models.EmailField(verbose_name="Email address", unique=True)
    patronymic = models.CharField(verbose_name="Patronymic", max_length=25, null=True, default=None)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.patronymic} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_staff



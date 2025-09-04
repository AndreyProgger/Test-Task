from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from blog_v2.models import Role


User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для описания ролей в системе"""
    class Meta:
        model = Role
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем пользовательские данные в полезную нагрузку
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        # Добавляем информацию о роли
        if user.role:
            token['role'] = user.role.name
            token['role_id'] = user.role.id
        else:
            token['role'] = 'user'  # Значение по умолчанию

        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'

        return token


class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализатор представляющий поля для создания пользователя """
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    patronymic = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm', 'patronymic']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        # Проверка совпадения паролей
        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # Получаем или создаем роль 'user'
        user_role, created = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Regular user with basic permissions'}
        )

        # Создаем пользователя с ролью
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=password,
            patronymic=validated_data.get('patronymic'),
            role=user_role,  # Присваиваем роль

        )

        return user


class LoginSerializer(serializers.Serializer):
    """ Сериализатор представляющий поля для входа пользователя в систему """
    email = serializers.EmailField()
    password = serializers.CharField()
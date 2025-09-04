from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    """Сериализатор для описания профиля пользователя"""
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.EmailField(read_only=True)
    patronymic = serializers.CharField(max_length=25)

from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    """Сериализатор для описания поста"""
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=600)

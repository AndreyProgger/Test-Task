from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

from .models import Post
from common.permissions import IsOwner, IsAdmin
from .serializers import PostSerializer

tags = ["blog"]


class PostListView(APIView):
    serializer_class = PostSerializer

    @extend_schema(
        summary="Retrieve all Posts from blog",
        description="""
                This endpoint allows to retrieve all posts for every consumer.
            """,
        tags=tags,
    )
    @permission_classes([AllowAny])
    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create new post in blog",
        description="""
                This endpoint allows a authenticated user to add new post.
            """,
        tags=tags,
    )
    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(
                {'error': 'Неверные данные', 'details': serializer.errors},
                status=400
            )


class PostDetailView(APIView):
    serializer_class = PostSerializer

    def get_object(self, pk):
        """ Вспомогательная функция для получения объекта по pk """
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve Post",
        description="""
                This endpoint allows an authenticated user to get detail information about the post.
            """,
        tags=tags,
    )
    @permission_classes([IsAuthenticated])
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    @extend_schema(
        summary="Edit Post",
        description="""
                This endpoint allows a owner to edit his post.
            """,
        tags=tags,
    )
    @permission_classes([IsOwner])
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        summary="Delete Post",
        description="""
                This endpoint allows a owner or admin to delete post.
            """,
        tags=tags,
    )
    @permission_classes([IsOwner, IsAdmin])
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=204)

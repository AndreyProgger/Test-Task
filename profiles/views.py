from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import set_dict_attr
from profiles.serializers import ProfileSerializer

tags = ["Profiles"]


class ProfileView(APIView):
    serializer_class = ProfileSerializer

    @extend_schema(
        summary="Retrieve Profile",
        description="""
            This endpoint allows a user to retrieve his/her profile.
        """,
        tags=tags,
    )
    def get(self, request):
        user = request.user

        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Update Profile",
        description="""
                This endpoint allows a user to update his/her profile.
            """,
        tags=tags,
        request={"multipart/form-data": serializer_class},
    )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = set_dict_attr(user, serializer.validated_data)
        user.save()
        serializer = self.serializer_class(user)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Deactivate account",
        description="""
            This endpoint allows a user to deactivate his/her account.
        """,
        tags=tags,
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data={"message": "User Account Deactivated"})
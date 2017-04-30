
# Create your views here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from json_api.JSONResponse import JSONResponse
from users.serializers import UserSerializer


@api_view(["POST"])
@authentication_classes(())
@permission_classes((AllowAny,))
def create_user(request):
    if request.method == "POST":
        user_serializer = UserSerializer(data=request.data["data"])
        if user_serializer.is_valid():
            User.objects.create_user(username=user_serializer.validated_data["username"], password=user_serializer.validated_data["password"])
            return Response(JSONResponse().addData("User", user_serializer.data).addData("status", "User created!").send(), status=status.HTTP_201_CREATED)
        else:
            return Response(JSONResponse().addError(0, "User could not be created").addError(1, user_serializer.errors).send(), status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authentication_classes(())
@permission_classes((AllowAny,))
def test_login(request):
    if User.objects.get_by_natural_key(request.data["username"]):
        return Response(True, status=status.HTTP_200_OK)
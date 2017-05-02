
# Create your views here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from json_api.JSONResponse import JSONResponse
from users.models import Keys
from users.serializers import UserSerializer, KeySerializer, InfoSerializer


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


@api_view(["POST"])
def create_key(request):
    if request.data["data"]:
        key_serializer = KeySerializer(data=request.data["data"])
        if key_serializer.is_valid():
            key_serializer.save()
            return Response(JSONResponse().addData("Key", key_serializer.data).
                            addData("status", "Key created!").
                            send(),
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                JSONResponse().addError(0, "Key could not be created").addError(1, key_serializer.errors).send(),
                status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
                JSONResponse().addError(0, "No data in request").send(),
                status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def list_keys(request):
    serializer = KeySerializer(Keys.objects.all(), many=True)
    return Response(JSONResponse().addData("Keys", serializer.data).send(),
                    status=status.HTTP_200_OK)

@api_view(["POST"])
def post_info(request):
    if request.data["data"]:
        info_serializer = InfoSerializer(data=request.data["data"])
        if info_serializer.is_valid():
            info_serializer.save(user=request.user)
            return Response(JSONResponse().addData("Information", info_serializer.data).
                            addData("status", "Information added to user " + request.user.username).
                            send(),
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                JSONResponse().addError(0, "Information could not be added").addError(1, info_serializer.errors).send(),
                status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
                JSONResponse().addError(0, "No data in request").send(),
                status=status.HTTP_400_BAD_REQUEST)
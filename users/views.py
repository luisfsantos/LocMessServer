
# Create your views here.
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from json_api.JSONResponse import JSONResponse
from location.serializers import UserLocationSerializer
from messaging.serializers import MessageSerializer
from users.models import Keys, Info
from users.serializers import UserSerializer, KeySerializer, InfoSerializer
from users.user_location import UserLocation


@api_view(["POST"])
@authentication_classes(())
@permission_classes((AllowAny,))
def create_user(request):
    if request.method == "POST":
        user_serializer = UserSerializer(data=request.data)
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


@api_view(['POST'])
def user_update_location(request):
    if request.data["data"]:
        user_location_serializer = UserLocationSerializer(data=request.data['data'])
        if user_location_serializer.is_valid():
            messages = UserLocation(request.user, user_location_serializer.validated_data).getMessages()
            messages_serializer = MessageSerializer(messages, many=True)
            return Response(JSONResponse().addData("Location", user_location_serializer.data).
                            addData("Messages", messages_serializer.data).
                            send(),
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                JSONResponse().addError(0, "User location could not be loaded").addError(1, user_location_serializer.errors).send(),
                status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
                JSONResponse().addError(0, "No data in request").send(),
                status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def delete_information(request, id):
    response = JSONResponse()
    with transaction.atomic():
        try:
            information = Info.objects.get(id=id, user=request.user)
            information.delete()
            return Response(response.addData("status", "completed deletion")
                            .addData(id, "Information with id: " + str(id) + " was deleted.")
                            .send(),
                    status=status.HTTP_200_OK)
        except Info.DoesNotExist:
            return Response(response.addError(0, "Information with id: " + str(id) + " does not exist or cannot be deleted").send(), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_information(request):
    serializer = InfoSerializer(Info.objects.filter(user=request.user), many=True)
    return Response(JSONResponse().addData("User Information", serializer.data).send(),
                    status=status.HTTP_200_OK)
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from json_api.JSONResponse import JSONResponse
from messaging.models import Message
from messaging.serializers import MessageSerializer


@api_view(["POST"])
def create_message(request):
    message_serializer = MessageSerializer(data=request.data["data"])
    if message_serializer.is_valid():
        m = message_serializer.save(user=request.user)
        return Response(JSONResponse().addData("Message", message_serializer.data).
                        addData("status", "Message created!").
                        send(),
                        status=status.HTTP_201_CREATED)
    else:
        return Response(
            JSONResponse().addError(0, "Message could not be created").addError(1, message_serializer.errors).send(),
            status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def list_messages(request):
    serializer = MessageSerializer(Message.objects.all(), many=True)
    return Response(JSONResponse().addData("Messages", serializer.data).send(),
                        status=status.HTTP_200_OK)
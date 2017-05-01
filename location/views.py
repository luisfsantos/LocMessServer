import json

from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from json_api.JSONResponse import JSONResponse
from location.models import Location
from location.serializers import LocationSerializer


@api_view(["POST"])
def create_location(request):
    serializer = LocationSerializer(data=request.data["data"])
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(JSONResponse().addData("Location", serializer.data).addData("status", "Location created!").send(),
                        status=status.HTTP_201_CREATED)
    else:
        return Response(
            JSONResponse().addError(0, "Location could not be created").addError(1, serializer.errors).send(),
            status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def list_locations(request):
    serializer = LocationSerializer(Location.objects.all(), many=True)
    return Response(JSONResponse().addData("Locations", serializer.data).send(),
                        status=status.HTTP_200_OK)

@api_view(["POST"])
def delete_location(request):
    data = request.data["data"]
    location_id = map(lambda x: x["id"], data["location"])
    response = JSONResponse()
    with transaction.atomic():
        i = 0
        for id in location_id:
            i += 1
            try:
                location = Location.objects.get(id=id)
                location.delete()
                response.addData(i, "Location with id: " + str(id) + " was deleted.")
            except Location.DoesNotExist:
                response.addError(i, "Location with id: " + str(id) + " does not exist.")
    return Response(response.addData("status", "completed deletion").send(),
                        status=status.HTTP_200_OK)
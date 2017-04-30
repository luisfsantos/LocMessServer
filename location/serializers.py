import json

from django.db import transaction
from rest_framework import serializers

import location
from location.models import Coordinate, WIFICoordinate, GPSCoordinate, SSID, Location


class GPSCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSCoordinate
        fields = '__all__'


class SSIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSID
        fields = ('name',)


class WIFICoordinateSerializer(serializers.ModelSerializer):
    wifiSSIDs = SSIDSerializer(source='ssid_set', many=True)
    class Meta:
        model = WIFICoordinate
        fields = '__all__'
        depth = 2


class CoordinateSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        if hasattr(instance, "gpscoordinate"):
            return GPSCoordinateSerializer(instance=instance.gpscoordinate).data
        elif hasattr(instance, "wificoordinate"):
            return WIFICoordinateSerializer(instance=instance.wificoordinate).data

    def to_internal_value(self, data):
        if data["type"] == location.models.GPS:
            serializer = GPSCoordinateSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                return serializer.validated_data
        elif data["type"] == location.models.WIFI:
            serializer = WIFICoordinateSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                return serializer.validated_data

    class Meta:
        model = Coordinate
        fields = '__all__'

class LocationSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    creation_date = serializers.DateTimeField()
    coordinate = CoordinateSerializer()
    author = serializers.CharField(source="author.username", read_only=True)

    def create(self, validated_data):
        with transaction.atomic():
            if(validated_data["coordinate"]["type"] == location.models.GPS):
                coordinate = GPSCoordinate.create(latitude=validated_data["coordinate"]["latitude"],
                                                  longitude=validated_data["coordinate"]["longitude"],
                                                  radius=validated_data["coordinate"]["radius"])
            elif(validated_data["coordinate"]["type"] == location.models.WIFI):
                coordinate = WIFICoordinate.create(ssids=map(lambda x: x["name"], validated_data["coordinate"]["ssid_set"]))

            return Location.objects.create(name = validated_data["name"], author = validated_data["user"], creation_date=validated_data["creation_date"], coordinate = coordinate)

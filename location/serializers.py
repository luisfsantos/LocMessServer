from rest_framework import serializers

from location.models import Coordinate, WIFICoordinate, GPSCoordinate, SSID


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

    class Meta:
        model = Coordinate
        fields = '__all__'

class LocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    creation_date = serializers.DateTimeField()
    coordinate = CoordinateSerializer()

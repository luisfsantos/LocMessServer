import datetime

import django
from django.contrib.auth.models import User
from django.db import models
from geopy.distance import vincenty

# Create your models here.
import location

EMPTY = 'Empty'
GPS = 'GPS'
WIFI = 'WIFI'

COORDINATE_TYPE = (
        (EMPTY, "Empty"),
        (GPS, "GPS"),
        (WIFI, "WIFI"),
    )

class Coordinate(models.Model):
    type = models.CharField(
        max_length=5,
        choices=COORDINATE_TYPE,
        default=EMPTY,
    )


class SSID(models.Model):
    coordinate = models.ForeignKey(Coordinate)
    name = models.CharField(max_length=50)

class GPSCoordinate(Coordinate):
    latitude = models.DecimalField(max_digits=30, decimal_places=20)
    longitude = models.DecimalField(max_digits=30, decimal_places=20)
    radius = models.DecimalField(max_digits=30, decimal_places=5)

    @classmethod
    def create(cls, latitude, longitude, radius):
        gps = GPSCoordinate.objects.create(type=GPS,
                                           latitude = latitude,
                                           longitude = longitude,
                                           radius = radius)
        return gps

    def in_range(self, user_location):
        user_at = (user_location['latitude'], user_location['longitude'])
        message_at = (self.latitude, self.longitude)
        return vincenty(user_at, message_at).meters <= self.radius

class WIFICoordinate(Coordinate):

    @classmethod
    def create(cls, ssids):
        wifi = WIFICoordinate.objects.create(type=WIFI)
        for ssid in ssids:
            ss = SSID.objects.create(name=ssid, coordinate=wifi)
            wifi.ssid_set.add(ss)

        return wifi

    def in_range(self, user_location):
        user_ssids = map(lambda x: x['ssid'], user_location)
        location_ssids = map(lambda  x: x.name, self.ssid_set.all())
        return len(set(user_ssids).intersection(location_ssids)) > 0

class Location(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    coordinate = models.OneToOneField(
        Coordinate,
        on_delete=models.CASCADE,
    )

    def is_valid(self, user_location):
        if hasattr(self.coordinate, "gpscoordinate"):
            return self.coordinate.gpscoordinate.in_range(user_location = user_location)
        elif hasattr(self.coordinate, "wificoordinate"):
            return self.coordinate.wificoordinate.in_range(user_location = user_location)
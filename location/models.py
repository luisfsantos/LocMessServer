import datetime

import django
from django.contrib.auth.models import User
from django.db import models

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

class WIFICoordinate(Coordinate):

    @classmethod
    def create(cls, ssids):
        wifi = WIFICoordinate.objects.create(type=WIFI)
        for ssid in ssids:
            ss = SSID.objects.create(name=ssid, coordinate=wifi)
            wifi.ssid_set.add(ss)

        return wifi
    pass

class Location(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    coordinate = models.OneToOneField(
        Coordinate,
        on_delete=models.CASCADE,
    )
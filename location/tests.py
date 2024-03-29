import json
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from rest_framework.parsers import JSONParser

import location
from location.models import Location, GPSCoordinate, WIFICoordinate
from location.serializers import LocationSerializer


class LocationTestCase(TestCase):
    ssids_arco = ["edurom", "thompson", "house"]
    location_gps = ["21.12222", "21.2", "11"]

    def setUp(self):
        User.objects.create_user(username="luissantos", password="somethingsafe")

    def test_gps_location_is_created(self):
        """Test that a gps location can be created"""
        u1 = User.objects.get(username="luissantos")
        location_name = "Arco do Cego"
        gps = GPSCoordinate.create(radius=self.location_gps[2],
                                           longitude=self.location_gps[1],
                                           latitude=self.location_gps[0])

        Location.objects.create(name=location_name, author = u1, coordinate=gps)
        l = Location.objects.get(name=location_name)


        self.assertEqual(l.name, location_name, "Correct location created")
        self.assertEqual(l.author.username, "luissantos", "Username of location creator")
        self.assertIsNotNone(l.coordinate, "Location has gps coordinate")
        self.assertEqual(l.coordinate.type, "GPS", "Correct coordinate added")
        self.assertTrue(hasattr(l.coordinate.gpscoordinate, "radius"), "GPS has radius")
        self.assertTrue(hasattr(l.coordinate.gpscoordinate, "longitude"), "GPS has longitude")
        self.assertTrue(hasattr(l.coordinate.gpscoordinate, "latitude"), "GPS has latitude")
        self.assertEqual(l.coordinate.gpscoordinate.latitude, Decimal(self.location_gps[0]), "latitude is correct")


    def test_wifi_location_is_created(self):
        """Test that a wifi location can be created"""
        u1 = User.objects.get(username="luissantos")
        location_name = "Arco do CegoS"
        wifi = WIFICoordinate.create(ssids=self.ssids_arco)
        Location.objects.create(name=location_name, author = u1, coordinate = wifi)
        l = Location.objects.get(name=location_name)
        self.assertEqual(l.name, location_name, "Correct location created")
        self.assertEqual(l.coordinate.type, "WIFI", "Correct coordinate added")
        for ssid in l.coordinate.wificoordinate.ssid_set.all():
            self.assertIn(ssid.name, self.ssids_arco, "The ssids are persisted")


    def test_wifi_location_from_json(self):
        """Test that a wifi location can be deserialized from json"""
        location_name = "Arco do CegoS"
        request = {"name": location_name, "creation_date": "2017-04-30T14:19:35.505954Z", "coordinate": {"wifiSSIDs": [{"name": "edurom"}, {"name": "thompson"}, {"name": "house"}], "type": "WIFI"}}
        #data = JSONParser().parse(json)
        serializer = LocationSerializer(data=request)
        if serializer.is_valid():
            u1 = User.objects.get(username="luissantos")
            serializer.save(user=u1)
            l = Location.objects.get(name=location_name)
            self.assertEqual(l.name, location_name, "Correct location created")
            self.assertEqual(l.coordinate.type, "WIFI", "Correct coordinate added")
            for ssid in l.coordinate.wificoordinate.ssid_set.all():
                self.assertIn(ssid.name, self.ssids_arco, "The ssids are persisted")

        else:
            self.fail(serializer.errors)
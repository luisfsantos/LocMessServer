import json

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from location.models import GPSCoordinate, Location
from messaging.models import Message
from messaging.serializers import MessageSerializer
from users.models import Keys, Info
from users.user_location import UserLocation


class MessageTestCase(TestCase):
    ssids_arco = ["edurom", "thompson", "house"]
    location_gps = ["21.12222", "21.2", "11"]

    def setUp(self):
        self.u = User.objects.create_user(username="luissantos", password="somethingsafe")
        gps = GPSCoordinate.create(radius=self.location_gps[2],
                                   longitude=self.location_gps[1],
                                   latitude=self.location_gps[0])

        self.l = Location.objects.create(name="Arco do Cego", author=self.u, coordinate=gps)
        self.key = Keys.objects.create(name="clube")
        Info.objects.create(key=self.key, user=self.u, value="sporting")

    def test_message_is_created(self):
        """Test that a message can be created"""
        message_title = "Arco do Cego"
        message_text = "Arco do Cego, os parque!!"
        message = Message.objects.create(title = message_title,
                                             text=message_text,
                                             location=self.l,
                                         author = self.u)

    def test_message_creation_from_json(self):
        json = {"title": "Arco do Cego", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z", "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1}, "whitelist": [{"key": "clube", "value" : "benfica"}], "blacklist": []}
        message_serializer = MessageSerializer(data=json)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            self.assertEqual(m.title, "Arco do Cego", "Title matches!")
            self.assertEqual(m.text, "Arco do Cego, os parque!!")
            self.assertEqual(m.author.username, "luissantos")
            for item in m.whitelist.all():
                self.assertEqual(item.key.id, 1)
        else:
            self.fail(message_serializer.errors)

    def test_user_get_message_blacklist(self):
        json = [{"title": "CasaCatarina", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z",
                "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                "whitelist": [], "blacklist": [{"key": "clube", "value": "sporting"}]},
                {"title": "CasaLuis", "text": "Arco do Cego, os parque!!",
                 "fromDate": "2017-05-01T18:42:15.703112Z",
                 "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                 "whitelist": [], "blacklist": [{"key": "clube", "value": "benfica"}]}
                ]
        message_serializer = MessageSerializer(data=json, many=True)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            messages = UserLocation(self.u, {"gps": {"radius": self.location_gps[2],
                                       "longitude": self.location_gps[1],
                                       "latitude": self.location_gps[0]}, "wifi":[{"ssid": "edurom"}], "date":"2017-05-02T18:42:15.703122Z"}).getMessages()
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].title, "CasaLuis")
        else:
            self.fail(message_serializer.errors)

    def test_user_get_message_whitelist(self):
        json = [{"title": "CasaCatarina", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z",
                "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                "whitelist": [{"key": "clube", "value": "benfica"}], "blacklist": []},
                {"title": "CasaLuis", "text": "Arco do Cego, os parque!!",
                 "fromDate": "2017-05-01T18:42:15.703112Z",
                 "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                 "whitelist": [{"key": "clube", "value": "sporting"}], "blacklist": []},
                ]
        message_serializer = MessageSerializer(data=json, many=True)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            messages = UserLocation(self.u, {"gps": {"radius": self.location_gps[2],
                                       "longitude": self.location_gps[1],
                                       "latitude": self.location_gps[0]}, "wifi":[{"ssid": "edurom"}], "date":"2017-05-02T18:42:15.703122Z"}).getMessages()
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].title, "CasaLuis")
        else:
            self.fail(message_serializer.errors)

    def test_user_not_get_message_whitelist(self):
        json = [{"title": "CasaCatarina", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z",
                "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                "whitelist": [{"key": "clube", "value": "benfica"}], "blacklist": []},
                {"title": "CasaLuis", "text": "Arco do Cego, os parque!!",
                 "fromDate": "2017-05-01T18:42:15.703112Z",
                 "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                 "whitelist": [{"key": "clube", "value": "benfica"}], "blacklist": []},
                ]
        message_serializer = MessageSerializer(data=json, many=True)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            messages = UserLocation(self.u, {"gps": {"radius": self.location_gps[2],
                                       "longitude": self.location_gps[1],
                                       "latitude": self.location_gps[0]}, "wifi":[{"ssid": "edurom"}], "date":"2017-05-02T18:42:15.703122Z"}).getMessages()
            self.assertEqual(len(messages), 0)
        else:
            self.fail(message_serializer.errors)

    def test_user_not_get_message_blacklist(self):
        json = [{"title": "CasaCatarina", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z",
                "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                "whitelist": [{"key": "clube", "value": "benfica"}], "blacklist": []},
                {"title": "CasaLuis", "text": "Arco do Cego, os parque!!",
                 "fromDate": "2017-05-01T18:42:15.703112Z",
                 "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                 "whitelist": [], "blacklist": [{"key": "clube", "value": "sporting"}]},
                ]
        message_serializer = MessageSerializer(data=json, many=True)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            messages = UserLocation(self.u, {"gps": {"radius": self.location_gps[2],
                                       "longitude": self.location_gps[1],
                                       "latitude": self.location_gps[0]}, "wifi":[{"ssid": "edurom"}], "date":"2017-05-02T18:42:15.703122Z"}).getMessages()
            self.assertEqual(len(messages), 0)
        else:
            self.fail(message_serializer.errors)

    def test_user_not_get_message_wrong_date(self):
        json = [{"title": "CasaCatarina", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z",
                "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                "whitelist": [], "blacklist": []},
                {"title": "CasaLuis", "text": "Arco do Cego, os parque!!",
                 "fromDate": "2017-05-01T18:42:15.703112Z",
                 "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                 "whitelist": [], "blacklist": []},
                ]
        message_serializer = MessageSerializer(data=json, many=True)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            messages = UserLocation(self.u, {"gps": {"radius": self.location_gps[2],
                                       "longitude": self.location_gps[1],
                                       "latitude": self.location_gps[0]}, "wifi":[{"ssid": "edurom"}], "date":"2017-07-02T18:42:15.703122Z"}).getMessages()
            self.assertEqual(len(messages), 0)
        else:
            self.fail(message_serializer.errors)

    def test_user_get_message_no_filter(self):
        json = [
                {"title": "CasaLuis", "text": "Arco do Cego, os parque!!",
                 "fromDate": "2017-05-01T18:42:15.703112Z",
                 "toDate": "2017-06-01T18:42:15.703122Z", "location": {"id":1},
                 "whitelist": [], "blacklist": []},
                ]
        message_serializer = MessageSerializer(data=json, many=True)
        if message_serializer.is_valid():
            m = message_serializer.save(user=self.u)
            messages = UserLocation(self.u, {"gps": {"radius": self.location_gps[2],
                                       "longitude": self.location_gps[1],
                                       "latitude": self.location_gps[0]}, "wifi":[{"ssid": "edurom"}], "date":"2017-05-02T18:42:15.703122Z"}).getMessages()
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].title, "CasaLuis")
        else:
            self.fail(message_serializer.errors)
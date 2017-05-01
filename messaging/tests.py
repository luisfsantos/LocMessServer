import json

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from location.models import GPSCoordinate, Location
from messaging.models import Message
from messaging.serializers import MessageSerializer
from users.models import Keys


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

    def test_message_is_created(self):
        """Test that a message can be created"""
        message_title = "Arco do Cego"
        message_text = "Arco do Cego, os parque!!"
        message = Message.objects.create(title = message_title,
                                             text=message_text,
                                             location=self.l,
                                         author = self.u)
        print(json.dumps(MessageSerializer(message).data))

    def test_message_creation_from_json(self):
        json = {"title": "Arco do Cego", "text": "Arco do Cego, os parque!!", "fromDate": "2017-05-01T18:42:15.703112Z", "toDate": "2017-05-01T18:42:15.703122Z", "location_id": 1, "whitelist": [{"keyID": self.key.id, "value" : "benfica"}], "blacklist": []}
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
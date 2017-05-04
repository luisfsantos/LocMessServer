import json

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from users.models import Keys, Info
from users.serializers import InfoSerializer


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="luissantos", password="somethingsafe")
        User.objects.create_user(username="luissantos2", password="somethingsafe")
        self.key = Keys.objects.create(name="clube")

    def test_users_are_created(self):
        """Two distinct users are created"""
        l1 = User.objects.get(username="luissantos")
        l2 = User.objects.get(username="luissantos2")
        self.assertIsNotNone(l1, "luissantos exists")
        self.assertIsNotNone(l2, "luissantos2 exists")

    def test_info_added_programaticaly_and_serializer(self):
        """Info is created and serialized"""
        l1 = User.objects.get(username="luissantos")
        info = Info.objects.create(value = "benfica",
                                   user = l1,
                                   key = self.key)
        self.assertIsNotNone(l1, "luissantos2 exists")
        self.assertEqual(info.value, "benfica")
        self.assertEqual(info.key.name, "clube")

    def test_info_created_from_json(self):
        json = {"key": "clube", "user": "luissantos", "value": "benfica"}
        info_serializer = InfoSerializer(data= json)
        if info_serializer.is_valid():
            l1 = User.objects.get(username="luissantos")
            try:
                info_serializer.save(user=l1)
            except Keys.DoesNotExist as err:
                self.fail(err.args)

        else:
            self.fail(info_serializer.errors)
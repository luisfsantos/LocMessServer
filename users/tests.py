from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="luissantos", password="somethingsafe")
        User.objects.create_user(username="luissantos2", password="somethingsafe")

    def test_users_are_created(self):
        """Two distinct users are created"""
        l1 = User.objects.get(username="luissantos")
        l2 = User.objects.get(username="luissantos2")
        self.assertIsNotNone(l1, "luissantos exists")
        self.assertIsNotNone(l2, "luissantos2 exists")
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
import django

from location.models import Location
from users.models import Keys


class Message(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField()
    fromDate = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    toDate = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    location = models.ForeignKey(Location)


class Whitelist(models.Model):
    key = models.ForeignKey(Keys, related_name="+")
    value = models.CharField(max_length=100)
    message = models.ForeignKey(Message, related_name="whitelist")

class Blacklist(models.Model):
    key = models.ForeignKey(Keys, related_name="+")
    value = models.CharField(max_length=100)
    message = models.ForeignKey(Message, related_name="blacklist")
from django.contrib.auth.models import User
from django.db import models

class Keys(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Info(models.Model):
    value = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="info")
    key = models.ForeignKey(Keys, related_name="+")

    #class Meta:
    #    unique_together = (("user", "key"),)

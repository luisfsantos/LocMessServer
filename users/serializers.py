from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from users.models import Keys


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Keys
        fields = ('id', 'name')
        read_only_fields = ('id', )

    def create(self, validated_data):
        with transaction.atomic():
            return Keys.objects.create(name=validated_data['name'])
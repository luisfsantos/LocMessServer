from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from users.models import Keys, Info


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

class InfoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    key = serializers.CharField(source='key.name' )
    class Meta:
        model = Info
        fields = ('id', 'key', 'user', 'value')
        read_only_fields = ('id',)

    def validate_key(self, value):
        try:
            return Keys.objects.get(name=value)
        except Keys.DoesNotExist:
            return Keys.objects.create(name = value)

    def create(self, validated_data):
        with transaction.atomic():
            try:
                info = Info.objects.get(key = validated_data['key']['name'],
                                       user = validated_data['user'])
                info.value = validated_data['value']
                info.save()
                return info
            except Info.DoesNotExist:
                return Info.objects.create(key = validated_data['key']['name'],
                                       user = validated_data['user'],
                                       value = validated_data['value'])

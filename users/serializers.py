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

class KeyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keys
        fields = ('id', 'name')

    def to_internal_value(self, data):
        try:
            return Keys.objects.get(pk=data.get('id'))
        except Keys.DoesNotExist:
            return Keys.objects.create(name = data.get('name'))

class InfoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    key = KeyInfoSerializer()
    class Meta:
        model = Info
        fields = ('key', 'user', 'value')
        read_only_fields = ('user',)

    def create(self, validated_data):
        with transaction.atomic():
            return Info.objects.create(key = validated_data['key'],
                                       user = validated_data['user'],
                                       value = validated_data['value'])
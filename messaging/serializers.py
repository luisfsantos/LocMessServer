from django.db import transaction
from rest_framework import serializers

from location.models import Location
from messaging.models import Message, Whitelist, Blacklist
from users.models import Keys


class WhitelistSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='key.name')

    class Meta:
        model = Whitelist
        fields = ('key', 'value')

    def validate_key(self, value):
        try:
            Keys.objects.get(name=value)
            return value
        except Keys.DoesNotExist:
            raise serializers.ValidationError("key " + value + " does not exist")

class BlacklistSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source='key.name')

    class Meta:
        model = Blacklist
        fields = ('key', 'value')

    def validate_key(self, value):
        try:
            Keys.objects.get(name=value)
            return value
        except Keys.DoesNotExist:
            raise serializers.ValidationError("key " + value + " does not exist")


class MessageSerializer(serializers.ModelSerializer):
    location = serializers.IntegerField(source="location.id")
    whitelist = WhitelistSerializer(many=True)
    blacklist = BlacklistSerializer(many=True)

    class Meta:
        model = Message
        fields = ('id', 'title', 'text', 'fromDate', 'toDate', 'location', 'whitelist', 'blacklist')
        read_only_fields = ('id', )

    def validate_location(self, value):
        try:
            Location.objects.get(id=value)
            return value
        except Location.DoesNotExist:
            raise serializers.ValidationError("location does not exist")

    def create(self, validated_data):
        with transaction.atomic():
            message = Message.objects.create(title = validated_data['title'],
                                             text=validated_data['text'],
                                             fromDate=validated_data['fromDate'],
                                             toDate=validated_data['toDate'],
                                             location=Location.objects.get(id = validated_data['location']['id']),
                                             author = validated_data['user'])

            for value in validated_data["whitelist"]:
                Whitelist.objects.create(key=Keys.objects.get(name=value['key']['name']), value = value["value"], message = message)
            for value in validated_data["blacklist"]:
                Blacklist.objects.create(key=Keys.objects.get(name=value['key']['name']), value = value["value"], message = message)

            return message

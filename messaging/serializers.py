from django.db import transaction
from rest_framework import serializers

from location.models import Location
from messaging.models import Message, Whitelist, Blacklist
from users.models import Keys


class WhitelistSerializer(serializers.ModelSerializer):
    keyID = serializers.IntegerField(source='key.id')

    class Meta:
        model = Whitelist
        fields = ('keyID', 'value')

class BlacklistSerializer(serializers.ModelSerializer):
    keyID = serializers.IntegerField(source='key.id')

    class Meta:
        model = Blacklist
        fields = ('keyID', 'value')


class MessageSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(source="location.id")
    whitelist = WhitelistSerializer(many=True)
    blacklist = BlacklistSerializer(many=True)

    class Meta:
        model = Message
        fields = ('id', 'title', 'text', 'fromDate', 'toDate', 'location_id', 'whitelist', 'blacklist')
        read_only_fields = ('id', )

    def create(self, validated_data):
        with transaction.atomic():
            message = Message.objects.create(title = validated_data['title'],
                                             text=validated_data['text'],
                                             fromDate=validated_data['fromDate'],
                                             toDate=validated_data['toDate'],
                                             location=Location.objects.get(id = validated_data['location']['id']),
                                             author = validated_data['user'])

            for value in validated_data["whitelist"]:
                try:
                    Whitelist.objects.create(key=Keys.objects.get(id=value['key']['id']), value = value["value"], message = message)
                except Keys.DoesNotExist:
                    raise ValueError("keyID", value['key']['id'])
            for value in validated_data["blacklist"]:
                try:
                    Blacklist.objects.create(key=Keys.objects.get(id=value['keyID']['id']), value = value["value"], message = message)
                except Keys.DoesNotExist:
                    raise ValueError("keyID", value['key']['id'])

            return message

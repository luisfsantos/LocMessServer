import json

import location
from location.models import Location
from messaging.models import Message, Whitelist, Blacklist
from messaging.serializers import MessageSerializer
from users.serializers import InfoSerializer


class UserLocation():

    def __init__(self, user, current_location):
        self.user = user
        self.gps_location = current_location["gps"]
        self.wifi_location = current_location["wifi"]
        self.date = current_location["date"]

    def infomation_is_valid(self, message):
        user_info = self.user.info.all()
        for info in user_info:
            try:
                white = message.whitelist.get(key=info.key)
                if white.value != info.value:
                    return False
            except Whitelist.DoesNotExist:
                pass

            try:
                black = message.blacklist.get(key=info.key)
                if black.value == info.value:
                    return False
            except Blacklist.DoesNotExist:
                pass
        return True

    def location_in_range(self, message_location):
        coordinate_type = message_location.coordinate.type
        loc = []
        if coordinate_type == location.models.GPS:
            loc = self.gps_location
        elif coordinate_type == location.models.WIFI:
            loc = self.wifi_location

        return message_location.is_valid(user_location = loc)

    def getMessages(self):
        all_messages = Message.objects.filter(fromDate__lte = self.date, toDate__gte = self.date)
        user_messages = []
        for message in all_messages:
            if self.location_in_range(message_location = message.location) and self.infomation_is_valid(message = message):
                user_messages.append(message)
        return user_messages
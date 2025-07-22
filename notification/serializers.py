from rest_framework import serializers, exceptions

from .models import *



class NotificationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

    

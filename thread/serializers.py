from .models import *
from rest_framework import serializers


class ThreadSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Thread
        fields = "__all__"
        read_only_fields = ["user"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["thread","user"]


class ThreadSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadSubscription
        fields = "__all__"
        read_only_fields = ["thread","user"]
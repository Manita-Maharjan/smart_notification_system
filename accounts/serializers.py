from .models import *

from rest_framework import serializers, exceptions, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from utilities.common import sendSms
# from utilities.permission import has_dashboard_access
from utilities.error_handler import CustomValidation

from notification.models import Notification
from notification.tasks import send_notification


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField(default = True)

    class Meta:
        model = User
        fields = ['id','username','password','email','phone', 'phone_verified','image','first_name', 'last_name', 'is_active', 'created_at','deleted','deleted_at']
        read_only_fields = ['id', 'created_at','updated_at']

    def validate_username(self, value):
        """
        Check that the username is unique case insensitive
        """
        if User.objects.filter(username__iexact=value).count():
            raise CustomValidation('Username already exist.','username', status_code=status.HTTP_409_CONFLICT)
        return value

    def validate_email(self, value):
        """
        Check that the email is unique case insensitive
        """
        if User.objects.filter(email__iexact=value).count():
            raise CustomValidation('Email already exist.','email', status_code=status.HTTP_409_CONFLICT)
        return value
    
    def validate_phone(self, value):
        """
        Check that the email is unique case insensitive
        """
        if User.objects.filter(phone= value).exists():
            raise CustomValidation('This phone number already exist.','phone', status_code=status.HTTP_409_CONFLICT)
        return value
    

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if 'phone' in validated_data and not instance.phone == validated_data.get('phone'):
            instance.phone_verified = False
        return super().update(instance, validated_data)
    

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['phone'] = instance.phone if not instance.phone or (instance.phone and (self.context['request'].user == instance or  self.context['request'].user.is_superuser)) else str(instance.phone).replace(str(instance.phone)[4:8], "****")
        return data
    
    
    
class UserBriefSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = ['id', 'first_name','last_name','username','email','phone','phone_verified']




class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = LoginHistory
        fields = "__all__"



#custom jwt-authentication passing user info too 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        login_data = self.context['request'].data['device_info'] if 'device_info' in  self.context['request'].data else {}
        exists = LoginHistory.objects.filter(user=self.user,uuid=login_data.get('uuid'),device=login_data.get('device'),device_model=login_data.get('device_model'),os=login_data.get('os')).exists()
        login_data['user'] = self.user.id
        if not exists:
            login_serializer = LoginHistorySerializer(data=login_data)
            if login_serializer.is_valid():
                login_serializer.save()
                notification=Notification.objects.create(event_type = "new_login", message = f"A login from a new device was detected on your account.", user=self.user, status="sent")
                send_notification.delay(notification.id)
       
        refresh = self.get_token(self.user)

        serializer = UserBriefSerializer(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['user'] = serializer.data

        return data
    


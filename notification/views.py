from rest_framework import generics, permissions, status
from rest_framework.response import Response


from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from utilities.pagination import StandardResultsSetPagination
from utilities.permission import IsOwner
from .utils import *

from accounts.models import User

    
class NotificationPreferenceAPIView(generics.GenericAPIView):
    serializer_class = NotificationPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            pref = NotificationPreference.objects.get(user=self.request.user)
        except NotificationPreference.DoesNotExist:
            raise serializers.ValidationError({"error":"Notification preferences doesnot exists."})
        return pref
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        qs = Notification.objects.filter(user=self.request.user).order_by('-created_at')
        return qs


class NotificationUnreadListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsOwner]

    def get_queryset(self): 
        qs = Notification.objects.filter(user=self.request.user, is_read = False).order_by('-created_at')
        return qs
    

class NotificationMarkAsReadView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsOwner]                        
    
    def post(self, request):
        ids = request.data.get("ids", [])
        if not isinstance(ids, list):
            return Response({"error": "ids must be a list of notification IDs"},status=status.HTTP_400_BAD_REQUEST)
        
        qs = Notification.objects.filter(user=request.user, id__in=ids)
        valid_ids = set(qs.values_list('id', flat=True))
        invalid_ids = [i for i in ids if i not in valid_ids]

        if invalid_ids:
            return Response({"error": f"Invalid notification IDs for this user:{invalid_ids}"},status=status.HTTP_400_BAD_REQUEST)
        
        qs.update(is_read=True)
        serializer = NotificationSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


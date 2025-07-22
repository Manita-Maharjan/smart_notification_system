
from django.db.models import Q
from datetime import datetime, timedelta

from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from .models import *
from .serializers import *
from utilities.pagination import StandardResultsSetPagination
from utilities.permission import IsSuperUser, IsOwner


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        qs = User.objects.all().order_by('-created_at')

        if user: 
            qs = qs.filter(Q(username__icontains=user)|Q(email__icontains=user)|Q(phone__icontains=user)|Q(first_name__icontains=user)|Q(last_name__icontains=user)).order_by('-created_at')
        
        if not self.request.user.is_superuser:
            qs = qs.exclude(is_active = False)
        
        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update( { "request": self.request } )
        return context  


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): 
        qs = User.objects.get(id=self.request.user.id)
        return qs


class UserRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsSuperUser|IsOwner]

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        if self.request.user.is_superuser:
            if 'is_active' in request.data:
                user.is_active = request.data['is_active']
            user.save()
            return super().update(request, *args, **kwargs)

        if 'is_active' in request.data:
            raise PermissionDenied("Permission denied. Only superusers can modify 'is_active'.")

        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance or self.request.user.is_superuser: 
            instance.first_name = ""
            instance.last_name = ""
            instance.username = "deleted_" + str(instance.id)
            instance.email = ""
            instance.phone = 0
            instance.deleted = True
            instance.deleted_at= datetime.today()
            instance.image.delete(save=True)
            instance.image_url=None
            instance.bio = ""
            instance.is_active = False
            instance.socialaccount_set.all().delete()
            instance.save()
            return Response({"message": "Deleted successfully"},status=status.HTTP_200_OK)
        return Response('unable to proceed the request', status=status.HTTP_401_UNAUTHORIZED)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserLoginListCreateView(generics.ListCreateAPIView):
    queryset = LoginHistory.objects.all().order_by('-created_at')
    serializer_class = LoginHistorySerializer
    pagination_class = StandardResultsSetPagination
    lookup_url_kwarg = 'pk'
    
    def get_queryset(self): 
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        qs = LoginHistory.objects.filter(user_id=user_id).order_by('-created_at')
        return qs
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]



from rest_framework import generics, permissions
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from notification.models import *
from notification.tasks import send_notification


class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all().order_by('-created_at')
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ThreadRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(thread_id=self.kwargs.get('thread_pk')).order_by('-created_at')

    def perform_create(self, serializer):
        thread = get_object_or_404(Thread, pk=self.kwargs.get('thread_pk'))
        comment = serializer.save(user=self.request.user, thread=thread)
        subscribers = thread.subscribers
        for subscriber in subscribers:
            notification = Notification.objects.create(event_type = "new_comment", message = f"{self.request.user.username} posted a new comment: \'{comment.comment}\'", user=subscriber, status="sent")
            send_notification.delay(notification.id)



class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = ThreadSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ThreadSubscription.objects.filter(user=self.request.user,thread_id=self.kwargs.get('thread_pk'))

    def perform_create(self, serializer):
        thread = get_object_or_404(Thread, pk=self.kwargs.get('thread_pk'))
        serializer.save(user=self.request.user,thread=thread)


class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = ThreadSubscription.objects.all()
    serializer_class = ThreadSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ThreadSubscription.objects.filter(user=self.request.user)
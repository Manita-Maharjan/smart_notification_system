from django.urls import path
from notification.views import *

urlpatterns = [
    path('v1/notifications/history/', NotificationListView.as_view()),
    path('v1/notifications/unread/', NotificationUnreadListView.as_view()),
    path('v1/notifications/read/', NotificationMarkAsReadView.as_view()),
    path('v1/notifications/preferences/', NotificationPreferenceAPIView.as_view()),


]

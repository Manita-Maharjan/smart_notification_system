from django.db import models
from django.conf import settings

# from accounts.models import User, LoginHistory


CHANNEL_TYPES = [
    ("in_app", "In App"),
    ("email", "Email"),
    ("sms", "SMS"),
]

class NotificationPreference(models.Model):
    user = models.OneToOneField("accounts.user", on_delete=models.CASCADE, related_name="notification_pref")
    preferences = models.CharField(max_length=20, choices=CHANNEL_TYPES, default= "in_app")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Preferences"
    

class Notification(models.Model):
    EVENT_TYPES = [
    ("new_comment", "New Comment"),
    ("new_login", "New Login"),
    ("weekly_summary", "Weekly Summary"),
    ]

    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey("accounts.user", on_delete=models.CASCADE, related_name="notifications")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="sent")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.event_type} Notification"



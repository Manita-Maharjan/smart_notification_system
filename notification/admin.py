from django.urls import path
from django.shortcuts import redirect
from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Notification, NotificationPreference
from .tasks import send_notification



# admin.site.register(Notification)

admin.site.register(NotificationPreference)
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event_type', 'status')
    list_filter = ('status', 'event_type')

    
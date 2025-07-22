import logging
from celery import shared_task
from .models import *
from .utils import *

logger = logging.getLogger(__name__)

@shared_task
def send_notification(notif_ids):
    if isinstance(notif_ids, int):
        notif_ids = [notif_ids]
    notifications = Notification.objects.filter(id__in=notif_ids).select_related("user")

    for notif in notifications:
        user = notif.user
        try:
            pref = NotificationPreference.objects.filter(user=user).first()
            if not pref:
                notif.status = "failed"
                notif.save(update_fields=["status"])
                logger.warning(f"No NotificationPreference not found for user {user.username}. ")
                continue

            channel = pref.preferences
            sent = False

            if channel == "email":
                send_email(user, notif.message)
                sent = True
            elif channel == "sms":
                send_sms(user, notif.message)
                sent = True
            elif channel == "in_app":
                send_in_app_notification(user, notif.message)
                sent = True

            notif.status = "sent" if sent else "failed"
            notif.save(update_fields=["status"])

        except Exception as e:
            notif.status = "failed"
            notif.save(update_fields=["status"])
            logger.error(f"Failed to deliver notification {notif.id} to {user.username}: {e}", exc_info=True)

    return True

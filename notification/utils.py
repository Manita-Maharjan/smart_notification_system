import logging

logger = logging.getLogger(__name__)

def send_sms(user, message):
    logger.info(f"SMS sent to {user.username}: {message}")

def send_email(user, message):
    logger.info(f"Email sent to {user.username}: {message}")

def send_in_app_notification(user, message):
    logger.info(f"In-app notification sent to {user.username}: {message}")
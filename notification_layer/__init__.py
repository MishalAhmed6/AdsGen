"""
Notification Layer for AdsCompetitor

This module provides SMS and email notification capabilities using Twilio and SendGrid.
"""

from .core.notification_layer import NotificationLayer
from .models.notification_types import NotificationType, NotificationStatus
from .models.message_models import SMSMessage, EmailMessage
from .exceptions import NotificationError, ConfigurationError, ValidationError

__all__ = [
    "NotificationLayer",
    "NotificationType", 
    "NotificationStatus",
    "SMSMessage",
    "EmailMessage",
    "NotificationError",
    "ConfigurationError",
    "ValidationError"
]

__version__ = "1.0.0"

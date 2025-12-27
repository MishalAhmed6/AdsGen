"""
Notification type definitions and enums.
"""

from enum import Enum
from typing import Dict, Any


class NotificationType(Enum):
    """Types of notifications supported."""
    SMS = "sms"
    EMAIL = "email"


class NotificationStatus(Enum):
    """Status of notification delivery."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Priority levels for notifications."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class DeliveryChannel(Enum):
    """Available delivery channels."""
    TWILIO_SMS = "twilio_sms"
    SENDGRID_EMAIL = "sendgrid_email"


# Status mappings for better error handling
STATUS_MESSAGES: Dict[NotificationStatus, str] = {
    NotificationStatus.PENDING: "Notification is pending delivery",
    NotificationStatus.SENT: "Notification has been sent successfully",
    NotificationStatus.DELIVERED: "Notification has been delivered",
    NotificationStatus.FAILED: "Notification delivery failed",
    NotificationStatus.RETRYING: "Notification is being retried",
    NotificationStatus.CANCELLED: "Notification was cancelled"
}

# Priority weights for queue processing
PRIORITY_WEIGHTS: Dict[Priority, int] = {
    Priority.LOW: 1,
    Priority.NORMAL: 2,
    Priority.HIGH: 3,
    Priority.URGENT: 4
}

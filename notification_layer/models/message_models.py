"""
Message models for SMS and Email notifications.
"""

import re
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field

from .base import BaseNotificationModel, NotificationMetadata
from .notification_types import NotificationType, NotificationStatus, Priority
from ..exceptions import ValidationError


@dataclass
class SMSMessage(BaseNotificationModel):
    """Model for SMS messages."""
    to_phone: str
    message: str
    from_phone: Optional[str] = None
    media_urls: Optional[List[str]] = field(default_factory=list)
    status: NotificationStatus = NotificationStatus.PENDING
    priority: Priority = Priority.NORMAL
    metadata: Optional[NotificationMetadata] = None
    message_id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization processing."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = NotificationMetadata(created_at=self.created_at)
    
    def validate(self) -> None:
        """Validate SMS message data."""
        if not self.to_phone:
            raise ValidationError("Recipient phone number is required")
        
        if not self.message:
            raise ValidationError("SMS message content is required")
        
        # Basic phone number validation (can be enhanced)
        phone_pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(phone_pattern, self.to_phone.replace(' ', '').replace('-', '')):
            raise ValidationError("Invalid phone number format")
        
        if len(self.message) > 1600:  # SMS character limit
            raise ValidationError("SMS message too long (max 1600 characters)")
        
        # Validate media URLs if provided
        if self.media_urls:
            url_pattern = r'^https?://.+'
            for url in self.media_urls:
                if not re.match(url_pattern, url):
                    raise ValidationError(f"Invalid media URL: {url}")


@dataclass
class EmailMessage(BaseNotificationModel):
    """Model for email messages."""
    to_email: str
    subject: str
    content: str
    from_email: Optional[str] = None
    from_name: Optional[str] = None
    html_content: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    cc_emails: Optional[List[str]] = field(default_factory=list)
    bcc_emails: Optional[List[str]] = field(default_factory=list)
    reply_to: Optional[str] = None
    status: NotificationStatus = NotificationStatus.PENDING
    priority: Priority = Priority.NORMAL
    metadata: Optional[NotificationMetadata] = None
    message_id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization processing."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = NotificationMetadata(created_at=self.created_at)
    
    def validate(self) -> None:
        """Validate email message data."""
        if not self.to_email:
            raise ValidationError("Recipient email is required")
        
        if not self.subject:
            raise ValidationError("Email subject is required")
        
        if not self.content and not self.html_content:
            raise ValidationError("Email content or HTML content is required")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.to_email):
            raise ValidationError("Invalid email format")
        
        # Validate CC and BCC emails
        for email in self.cc_emails or []:
            if not re.match(email_pattern, email):
                raise ValidationError(f"Invalid CC email format: {email}")
        
        for email in self.bcc_emails or []:
            if not re.match(email_pattern, email):
                raise ValidationError(f"Invalid BCC email format: {email}")
        
        # Validate reply-to email
        if self.reply_to and not re.match(email_pattern, self.reply_to):
            raise ValidationError(f"Invalid reply-to email format: {self.reply_to}")


@dataclass
class NotificationResult:
    """Result of a notification attempt."""
    success: bool
    message_id: Optional[str] = None
    status: NotificationStatus = NotificationStatus.PENDING
    error_message: Optional[str] = None
    provider_response: Optional[Dict[str, Any]] = None
    delivery_time: Optional[datetime] = None
    retry_after: Optional[int] = None  # seconds to wait before retry
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "success": self.success,
            "message_id": self.message_id,
            "status": self.status.value,
            "error_message": self.error_message,
            "provider_response": self.provider_response,
            "delivery_time": self.delivery_time.isoformat() if self.delivery_time else None,
            "retry_after": self.retry_after
        }

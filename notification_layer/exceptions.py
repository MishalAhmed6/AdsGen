"""
Custom exceptions for the Notification Layer.
"""


class NotificationError(Exception):
    """Base exception for notification-related errors."""
    pass


class ConfigurationError(NotificationError):
    """Raised when there's a configuration issue."""
    pass


class ValidationError(NotificationError):
    """Raised when input validation fails."""
    pass


class SMSDeliveryError(NotificationError):
    """Raised when SMS delivery fails."""
    pass


class EmailDeliveryError(NotificationError):
    """Raised when email delivery fails."""
    pass


class RateLimitError(NotificationError):
    """Raised when rate limits are exceeded."""
    pass


class AuthenticationError(NotificationError):
    """Raised when authentication fails."""
    pass

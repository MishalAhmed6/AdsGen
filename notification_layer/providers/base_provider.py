"""
Base provider class for notification services.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.message_models import NotificationResult
from ..models.notification_types import NotificationType


class BaseNotificationProvider(ABC):
    """Base class for notification providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the provider with configuration.
        
        Args:
            config: Provider-specific configuration
        """
        self.config = config
        self._validate_config()
    
    @abstractmethod
    def _validate_config(self) -> None:
        """Validate provider configuration."""
        pass
    
    @abstractmethod
    def send_notification(self, message_data: Dict[str, Any]) -> NotificationResult:
        """
        Send a notification.
        
        Args:
            message_data: Message data to send
            
        Returns:
            NotificationResult with delivery status
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider."""
        pass
    
    @abstractmethod
    def get_supported_type(self) -> NotificationType:
        """Get the notification type this provider supports."""
        pass
    
    def is_enabled(self) -> bool:
        """Check if the provider is enabled."""
        return self.config.get("enabled", True)
    
    def get_rate_limit(self) -> int:
        """Get the rate limit for this provider."""
        return self.config.get("rate_limit_per_minute", 60)
    
    def get_timeout(self) -> float:
        """Get the timeout for this provider."""
        return self.config.get("timeout", 30.0)

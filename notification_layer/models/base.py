"""
Base model classes for the Notification Layer.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass


class BaseNotificationModel(ABC):
    """Base class for notification models."""
    
    def __init__(self, **kwargs):
        """Initialize the model with provided kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        return result
    
    @abstractmethod
    def validate(self) -> None:
        """Validate the model data."""
        pass
    
    def __repr__(self) -> str:
        """Return string representation of the model."""
        attrs = ', '.join(f"{k}={v}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"


@dataclass
class NotificationMetadata:
    """Metadata for notifications."""
    created_at: datetime
    updated_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    priority: str = "normal"  # low, normal, high
    tags: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        """Post-initialization processing."""
        if self.tags is None:
            self.tags = {}

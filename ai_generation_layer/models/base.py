"""
Base classes for AI Generation Layer providers and validators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ..exceptions import ProviderError, ContentValidationError


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the provider with configuration.
        
        Args:
            config: Configuration dictionary for the provider
        """
        self.config = config or {}
    
    @abstractmethod
    def generate_content(self, prompt: str, **kwargs) -> str:
        """
        Generate content using the LLM provider.
        
        Args:
            prompt: The prompt to send to the LLM
            **kwargs: Additional parameters for the LLM
            
        Returns:
            Generated content as string
            
        Raises:
            ProviderError: If generation fails
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available and properly configured.
        
        Returns:
            True if available, False otherwise
        """
        pass
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with default fallback.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)


class BaseContentValidator(ABC):
    """Abstract base class for content validators."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the validator with configuration.
        
        Args:
            config: Configuration dictionary for the validator
        """
        self.config = config or {}
    
    @abstractmethod
    def validate_content(self, content: str, content_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate generated content.
        
        Args:
            content: The content to validate
            content_type: Type of content (headline, ad_text, hashtags, cta)
            context: Marketing context for validation
            
        Returns:
            Validation results dictionary
            
        Raises:
            ContentValidationError: If validation fails
        """
        pass
    
    @abstractmethod
    def calculate_quality_score(self, content: str, content_type: str, context: Dict[str, Any]) -> float:
        """
        Calculate quality score for content.
        
        Args:
            content: The content to score
            content_type: Type of content
            context: Marketing context for scoring
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        pass
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with default fallback.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)

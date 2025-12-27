"""
Custom exceptions for the AI Generation Layer module.
"""


class AIGenerationError(Exception):
    """Base exception for AI Generation Layer module."""
    pass


class ProviderError(AIGenerationError):
    """Raised when LLM provider operations fail."""
    pass


class ContentValidationError(AIGenerationError):
    """Raised when content validation fails."""
    pass


class PromptError(AIGenerationError):
    """Raised when prompt generation or processing fails."""
    pass


class ConfigurationError(AIGenerationError):
    """Raised when configuration is invalid."""
    pass

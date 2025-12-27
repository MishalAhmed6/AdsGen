"""
Custom exceptions for the Input Layer module.
"""


class InputLayerError(Exception):
    """Base exception for Input Layer module."""
    pass


class ValidationError(InputLayerError):
    """Raised when input validation fails."""
    pass


class ProcessingError(InputLayerError):
    """Raised when data processing fails."""
    pass


class ConfigurationError(InputLayerError):
    """Raised when configuration is invalid."""
    pass

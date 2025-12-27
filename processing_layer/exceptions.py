"""
Custom exceptions for the Processing Layer module.
"""


class ProcessingLayerError(Exception):
    """Base exception for Processing Layer module."""
    pass


class AnalysisError(ProcessingLayerError):
    """Raised when analysis operations fail."""
    pass


class ContextBuildingError(ProcessingLayerError):
    """Raised when context building fails."""
    pass


class ToneAnalysisError(AnalysisError):
    """Raised when tone analysis fails."""
    pass


class KeywordExtractionError(AnalysisError):
    """Raised when keyword extraction fails."""
    pass


class RegionalAnalysisError(AnalysisError):
    """Raised when regional analysis fails."""
    pass

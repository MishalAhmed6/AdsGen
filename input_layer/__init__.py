"""
Input Layer Module

A modular input processing system for competitor analysis that handles:
- Competitor names
- Hashtags 
- ZIP codes

Features:
- Data cleaning and normalization
- Validation and error handling
- Extensible architecture for API/UI integration
"""

from .core.input_layer import InputLayer
from .handlers.competitor_handler import CompetitorHandler
from .handlers.hashtag_handler import HashtagHandler
from .handlers.zipcode_handler import ZipCodeHandler
from .models.input_types import InputData, ProcessedData, ValidationResult, InputType, ProcessingStatus
from .exceptions import InputLayerError, ValidationError, ProcessingError

__version__ = "1.0.0"
__all__ = [
    "InputLayer",
    "CompetitorHandler", 
    "HashtagHandler",
    "ZipCodeHandler",
    "InputData",
    "ProcessedData", 
    "ValidationResult",
    "InputType",
    "ProcessingStatus",
    "InputLayerError",
    "ValidationError",
    "ProcessingError"
]

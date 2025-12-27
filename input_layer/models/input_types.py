"""
Data type definitions for Input Layer processing.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class InputType(Enum):
    """Types of input data supported."""
    COMPETITOR_NAME = "competitor_name"
    HASHTAG = "hashtag"
    ZIP_CODE = "zip_code"


class ProcessingStatus(Enum):
    """Status of processing operations."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATION_ERROR = "validation_error"


@dataclass
class InputData:
    """Raw input data structure."""
    data: str
    input_type: InputType
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.input_type, str):
            self.input_type = InputType(self.input_type)


@dataclass 
class ValidationResult:
    """Result of validation operations."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def add_error(self, error: str) -> None:
        """Add a validation error."""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str) -> None:
        """Add a validation warning."""
        self.warnings.append(warning)
    
    def add_suggestion(self, suggestion: str) -> None:
        """Add a validation suggestion."""
        self.suggestions.append(suggestion)


@dataclass
class ProcessedData:
    """Processed and validated data structure."""
    original_data: str
    processed_data: str
    input_type: InputType
    status: ProcessingStatus
    validation_result: ValidationResult
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization."""
        return {
            "original_data": self.original_data,
            "processed_data": self.processed_data,
            "input_type": self.input_type.value,
            "status": self.status.value,
            "validation_result": {
                "is_valid": self.validation_result.is_valid,
                "errors": self.validation_result.errors,
                "warnings": self.validation_result.warnings,
                "suggestions": self.validation_result.suggestions
            },
            "metadata": self.metadata,
            "processing_timestamp": self.processing_timestamp
        }

"""
Competitor name handler for cleaning and validation.
"""

import re
import string
from typing import Dict, Any, List
from datetime import datetime

from ..models.base import BaseHandler
from ..models.input_types import InputData, ProcessedData, ValidationResult, ProcessingStatus, InputType
from ..exceptions import ValidationError, ProcessingError


class CompetitorHandler(BaseHandler):
    """Handler for competitor name processing."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize competitor handler with configuration.
        
        Args:
            config: Configuration dictionary with options:
                - min_length: Minimum name length (default: 2)
                - max_length: Maximum name length (default: 100)
                - allow_numbers: Allow numbers in names (default: False)
                - allowed_special_chars: Allowed special characters (default: " &.-'")
                - normalize_case: Normalize to title case (default: True)
                - remove_extra_spaces: Remove extra whitespace (default: True)
        """
        super().__init__(config)
        self.min_length = self.config.get("min_length", 2)
        self.max_length = self.config.get("max_length", 100)
        self.allow_numbers = self.config.get("allow_numbers", False)
        self.allowed_special_chars = self.config.get("allowed_special_chars", " &.-'")
        self.normalize_case = self.config.get("normalize_case", True)
        self.remove_extra_spaces = self.config.get("remove_extra_spaces", True)
        
        # Build character validation regex
        self._build_validation_pattern()
    
    def _build_validation_pattern(self) -> None:
        """Build regex pattern for character validation."""
        # Build pattern parts to avoid regex warnings
        pattern_parts = [r"a-zA-Z"]
        
        if self.allow_numbers:
            pattern_parts.append(r"0-9")
        
        # Add allowed special characters
        if self.allowed_special_chars:
            escaped_chars = re.escape(self.allowed_special_chars)
            pattern_parts.append(escaped_chars)
        
        pattern = "".join(pattern_parts)
        self.valid_char_pattern = re.compile(f"^[{pattern}\\s]+$")
    
    def validate(self, data: InputData) -> ValidationResult:
        """
        Validate competitor name.
        
        Args:
            data: InputData containing competitor name
            
        Returns:
            ValidationResult with validation status and messages
        """
        result = ValidationResult(is_valid=True)
        name = data.data.strip()
        
        # Length validation
        if len(name) < self.min_length:
            result.add_error(f"Name too short. Minimum length is {self.min_length} characters.")
        
        if len(name) > self.max_length:
            result.add_error(f"Name too long. Maximum length is {self.max_length} characters.")
        
        # Character validation
        if not self.valid_char_pattern.match(name):
            invalid_chars = set(name) - set(string.ascii_letters + string.digits + self.allowed_special_chars + " ")
            if invalid_chars:
                result.add_error(f"Invalid characters found: {', '.join(invalid_chars)}")
        
        # Business logic validations
        if not any(c.isalpha() for c in name):
            result.add_error("Name must contain at least one letter.")
        
        # Check for common issues
        if name.lower() in ["company", "business", "corp", "inc", "llc", "ltd"]:
            result.add_warning("Name appears to be a generic business term.")
        
        # Suggest improvements
        if name and not name[0].isupper() and self.normalize_case:
            result.add_suggestion("Consider capitalizing the first letter.")
        
        return result
    
    def clean(self, data: str) -> str:
        """
        Clean and normalize competitor name.
        
        Args:
            data: Raw competitor name
            
        Returns:
            Cleaned competitor name
        """
        # Remove leading/trailing whitespace
        cleaned = data.strip()
        
        # Remove extra whitespace if configured
        if self.remove_extra_spaces:
            cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove invalid characters (keep only valid ones)
        valid_chars = set(string.ascii_letters + string.digits + self.allowed_special_chars + " ")
        cleaned = ''.join(c for c in cleaned if c in valid_chars)
        
        # Normalize case if configured
        if self.normalize_case:
            cleaned = self._normalize_case(cleaned)
        
        return cleaned.strip()
    
    def _normalize_case(self, name: str) -> str:
        """
        Normalize case of competitor name.
        
        Args:
            name: Name to normalize
            
        Returns:
            Name with normalized case
        """
        # Handle special cases like "McDonald's", "O'Reilly", etc.
        special_prefixes = ["mc", "mac", "o'", "d'", "de", "la", "le", "van", "von"]
        
        words = name.split()
        normalized_words = []
        
        for i, word in enumerate(words):
            if not word:
                continue
                
            # Check for special prefixes
            lower_word = word.lower()
            for prefix in special_prefixes:
                if lower_word.startswith(prefix) and len(word) > len(prefix):
                    normalized_words.append(prefix.title() + word[len(prefix):].title())
                    break
            else:
                # Regular word - capitalize first letter
                normalized_words.append(word.title())
        
        return ' '.join(normalized_words)
    
    def process(self, data: InputData) -> ProcessedData:
        """
        Process competitor name through validation and cleaning.
        
        Args:
            data: InputData containing competitor name
            
        Returns:
            ProcessedData with results
        """
        if data.input_type != InputType.COMPETITOR_NAME:
            raise ProcessingError(f"Invalid input type {data.input_type} for CompetitorHandler")
        
        # Clean the data first
        cleaned_data = self.clean(data.data)
        
        # Create new InputData with cleaned data for validation
        cleaned_input = InputData(
            data=cleaned_data,
            input_type=data.input_type,
            metadata=data.metadata
        )
        
        # Validate the cleaned data
        validation_result = self.validate(cleaned_input)
        
        # Determine status
        if validation_result.is_valid:
            status = ProcessingStatus.COMPLETED
        elif validation_result.errors:
            status = ProcessingStatus.VALIDATION_ERROR
        else:
            status = ProcessingStatus.COMPLETED  # Has warnings but is valid
        
        return ProcessedData(
            original_data=data.data,
            processed_data=cleaned_data,
            input_type=data.input_type,
            status=status,
            validation_result=validation_result,
            metadata={
                **data.metadata,
                "handler": "CompetitorHandler",
                "config": self.config
            },
            processing_timestamp=datetime.now().isoformat()
        )

"""
Hashtag handler for cleaning and validation.
"""

import re
import string
from typing import Dict, Any, List, Set
from datetime import datetime

from ..models.base import BaseHandler
from ..models.input_types import InputData, ProcessedData, ValidationResult, ProcessingStatus, InputType
from ..exceptions import ValidationError, ProcessingError


class HashtagHandler(BaseHandler):
    """Handler for hashtag processing."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize hashtag handler with configuration.
        
        Args:
            config: Configuration dictionary with options:
                - min_length: Minimum hashtag length without # (default: 1)
                - max_length: Maximum hashtag length without # (default: 100)
                - allow_numbers: Allow numbers in hashtags (default: True)
                - allow_underscores: Allow underscores (default: True)
                - normalize_case: Normalize case (default: True)
                - remove_duplicates: Remove duplicate hashtags (default: True)
                - max_hashtags: Maximum number of hashtags (default: 30)
                - forbidden_words: List of forbidden words to flag
        """
        super().__init__(config)
        self.min_length = self.config.get("min_length", 1)
        self.max_length = self.config.get("max_length", 100)
        self.allow_numbers = self.config.get("allow_numbers", True)
        self.allow_underscores = self.config.get("allow_underscores", True)
        self.normalize_case = self.config.get("normalize_case", True)
        self.remove_duplicates = self.config.get("remove_duplicates", True)
        self.max_hashtags = self.config.get("max_hashtags", 30)
        self.forbidden_words = set(self.config.get("forbidden_words", []))
        
        # Build validation patterns
        self._build_validation_patterns()
    
    def _build_validation_patterns(self) -> None:
        """Build regex patterns for hashtag validation."""
        # Base pattern for hashtag characters
        char_pattern_parts = [r"a-zA-Z"]
        if self.allow_numbers:
            char_pattern_parts.append(r"0-9")
        if self.allow_underscores:
            char_pattern_parts.append(r"_")
        
        char_pattern = "".join(char_pattern_parts)
        
        # Pattern for individual hashtag
        self.hashtag_pattern = re.compile(f"^#[{char_pattern}]+$")
        
        # Pattern to extract hashtags from text
        self.extract_pattern = re.compile(r"#[\w]+")
    
    def validate(self, data: InputData) -> ValidationResult:
        """
        Validate hashtag(s).
        
        Args:
            data: InputData containing hashtag(s)
            
        Returns:
            ValidationResult with validation status and messages
        """
        result = ValidationResult(is_valid=True)
        text = data.data.strip()
        
        # Extract hashtags from text
        hashtags = self._extract_hashtags(text)
        
        if not hashtags:
            result.add_error("No valid hashtags found in input.")
            return result
        
        # Check maximum number of hashtags
        if len(hashtags) > self.max_hashtags:
            result.add_error(f"Too many hashtags. Maximum allowed is {self.max_hashtags}.")
        
        # Validate each hashtag
        for hashtag in hashtags:
            self._validate_single_hashtag(hashtag, result)
        
        # Check for duplicates if not removing them
        if not self.remove_duplicates:
            unique_hashtags = set(hashtags)
            if len(unique_hashtags) != len(hashtags):
                result.add_warning("Duplicate hashtags found.")
        
        return result
    
    def _validate_single_hashtag(self, hashtag: str, result: ValidationResult) -> None:
        """
        Validate a single hashtag.
        
        Args:
            hashtag: Hashtag to validate (including #)
            result: ValidationResult to update
        """
        # Check format
        if not self.hashtag_pattern.match(hashtag):
            result.add_error(f"Invalid hashtag format: {hashtag}")
            return
        
        # Check length (without #)
        content = hashtag[1:]
        if len(content) < self.min_length:
            result.add_error(f"Hashtag too short: {hashtag}")
        
        if len(content) > self.max_length:
            result.add_error(f"Hashtag too long: {hashtag}")
        
        # Check for forbidden words
        content_lower = content.lower()
        if content_lower in self.forbidden_words:
            result.add_error(f"Forbidden word in hashtag: {hashtag}")
        
        # Check for common issues
        if content.isdigit():
            result.add_warning(f"Hashtag contains only numbers: {hashtag}")
        
        if content.isupper() and len(content) > 3:
            result.add_suggestion(f"Consider using mixed case for readability: {hashtag}")
        
        # Check for common misspellings or issues
        if content_lower in ["hashtag", "tag", "tags"]:
            result.add_warning(f"Generic hashtag detected: {hashtag}")
    
    def clean(self, data: str) -> str:
        """
        Clean and normalize hashtag(s).
        
        Args:
            data: Raw hashtag data
            
        Returns:
            Cleaned hashtag string
        """
        # Extract hashtags from text
        hashtags = self._extract_hashtags(data)
        
        if not hashtags:
            return ""
        
        # Clean each hashtag
        cleaned_hashtags = []
        for hashtag in hashtags:
            cleaned = self._clean_single_hashtag(hashtag)
            if cleaned:
                cleaned_hashtags.append(cleaned)
        
        # Remove duplicates if configured
        if self.remove_duplicates:
            # Preserve order while removing duplicates
            seen = set()
            unique_hashtags = []
            for hashtag in cleaned_hashtags:
                if hashtag.lower() not in seen:
                    seen.add(hashtag.lower())
                    unique_hashtags.append(hashtag)
            cleaned_hashtags = unique_hashtags
        
        # Limit number of hashtags
        cleaned_hashtags = cleaned_hashtags[:self.max_hashtags]
        
        return " ".join(cleaned_hashtags)
    
    def _clean_single_hashtag(self, hashtag: str) -> str:
        """
        Clean a single hashtag.
        
        Args:
            hashtag: Hashtag to clean
            
        Returns:
            Cleaned hashtag
        """
        if not hashtag.startswith("#"):
            hashtag = "#" + hashtag
        
        # Remove invalid characters
        content = hashtag[1:]
        cleaned_content = ""
        
        for char in content:
            if char.isalnum() or (self.allow_underscores and char == "_"):
                cleaned_content += char
        
        # Normalize case
        if self.normalize_case and cleaned_content:
            # Use title case for readability
            cleaned_content = cleaned_content.title()
        
        return "#" + cleaned_content if cleaned_content else ""
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text.
        
        Args:
            text: Text containing hashtags
            
        Returns:
            List of hashtags found
        """
        hashtags = self.extract_pattern.findall(text)
        return hashtags
    
    def process(self, data: InputData) -> ProcessedData:
        """
        Process hashtag(s) through validation and cleaning.
        
        Args:
            data: InputData containing hashtag(s)
            
        Returns:
            ProcessedData with results
        """
        if data.input_type != InputType.HASHTAG:
            raise ProcessingError(f"Invalid input type {data.input_type} for HashtagHandler")
        
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
        
        # Extract hashtags for metadata
        extracted_hashtags = self._extract_hashtags(cleaned_data)
        
        return ProcessedData(
            original_data=data.data,
            processed_data=cleaned_data,
            input_type=data.input_type,
            status=status,
            validation_result=validation_result,
            metadata={
                **data.metadata,
                "handler": "HashtagHandler",
                "config": self.config,
                "hashtag_count": len(extracted_hashtags),
                "extracted_hashtags": extracted_hashtags
            },
            processing_timestamp=datetime.now().isoformat()
        )

"""
ZIP code handler for cleaning and validation.
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.base import BaseHandler
from ..models.input_types import InputData, ProcessedData, ValidationResult, ProcessingStatus, InputType
from ..exceptions import ValidationError, ProcessingError


class ZipCodeHandler(BaseHandler):
    """Handler for ZIP code processing."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize ZIP code handler with configuration.
        
        Args:
            config: Configuration dictionary with options:
                - supported_formats: List of supported formats (default: ["5", "5+4", "9"])
                - normalize_format: Format to normalize to (default: "5+4")
                - country: Country code for validation (default: "US")
                - validate_existence: Whether to validate ZIP code existence (default: False)
                - allow_international: Allow international postal codes (default: False)
                - strict_validation: Use strict validation rules (default: True)
        """
        super().__init__(config)
        self.supported_formats = self.config.get("supported_formats", ["5", "5+4", "9"])
        self.normalize_format = self.config.get("normalize_format", "5+4")
        self.country = self.config.get("country", "US")
        self.validate_existence = self.config.get("validate_existence", False)
        self.allow_international = self.config.get("allow_international", False)
        self.strict_validation = self.config.get("strict_validation", True)
        
        # Build validation patterns
        self._build_validation_patterns()
    
    def _build_validation_patterns(self) -> None:
        """Build regex patterns for ZIP code validation."""
        # US ZIP code patterns
        self.patterns = {
            "5": re.compile(r"^\d{5}$"),  # 12345
            "5+4": re.compile(r"^\d{5}-\d{4}$"),  # 12345-6789
            "9": re.compile(r"^\d{9}$"),  # 123456789
            "basic": re.compile(r"^\d{5}(-\d{4})?$")  # Either 5 or 5+4
        }
        
        # Canadian postal code pattern (A1A 1A1)
        self.canadian_pattern = re.compile(r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$")
        
        # General international pattern (basic validation)
        self.international_pattern = re.compile(r"^[A-Za-z0-9\s-]{3,10}$")
    
    def validate(self, data: InputData) -> ValidationResult:
        """
        Validate ZIP code.
        
        Args:
            data: InputData containing ZIP code
            
        Returns:
            ValidationResult with validation status and messages
        """
        result = ValidationResult(is_valid=True)
        zip_code = data.data.strip()
        
        if not zip_code:
            result.add_error("ZIP code cannot be empty.")
            return result
        
        # Determine format and validate
        format_type = self._detect_format(zip_code)
        
        if format_type == "invalid":
            result.add_error(f"Invalid ZIP code format: {zip_code}")
            return result
        
        # Validate based on detected format
        if not self._validate_format(zip_code, format_type):
            result.add_error(f"ZIP code format validation failed: {zip_code}")
        
        # Additional validations
        self._validate_checksum(zip_code, result)
        self._validate_geographic_ranges(zip_code, result)
        
        # Check if format is in supported formats
        if format_type not in self.supported_formats:
            result.add_warning(f"ZIP code format '{format_type}' not in supported formats: {self.supported_formats}")
        
        # Suggest normalization
        if self.normalize_format != format_type:
            normalized = self._normalize_format(zip_code, self.normalize_format)
            if normalized != zip_code:
                result.add_suggestion(f"Consider normalizing to: {normalized}")
        
        return result
    
    def _detect_format(self, zip_code: str) -> str:
        """
        Detect ZIP code format.
        
        Args:
            zip_code: ZIP code to analyze
            
        Returns:
            Format type string
        """
        zip_code = zip_code.strip()
        
        # Check US formats
        if self.patterns["5"].match(zip_code):
            return "5"
        elif self.patterns["5+4"].match(zip_code):
            return "5+4"
        elif self.patterns["9"].match(zip_code):
            return "9"
        elif self.canadian_pattern.match(zip_code):
            return "canadian"
        elif self.allow_international and self.international_pattern.match(zip_code):
            return "international"
        else:
            return "invalid"
    
    def _validate_format(self, zip_code: str, format_type: str) -> bool:
        """
        Validate ZIP code against specific format.
        
        Args:
            zip_code: ZIP code to validate
            format_type: Expected format type
            
        Returns:
            True if valid, False otherwise
        """
        if format_type in ["5", "5+4", "9"]:
            return self.patterns[format_type].match(zip_code) is not None
        elif format_type == "canadian":
            return self.canadian_pattern.match(zip_code) is not None
        elif format_type == "international":
            return self.international_pattern.match(zip_code) is not None
        
        return False
    
    def _validate_checksum(self, zip_code: str, result: ValidationResult) -> None:
        """
        Validate ZIP code checksum (basic validation).
        
        Args:
            zip_code: ZIP code to validate
            result: ValidationResult to update
        """
        if not self.strict_validation:
            return
        
        # Extract 5-digit portion for validation
        five_digit = self._extract_five_digit(zip_code)
        if not five_digit:
            return
        
        # Basic checksum validation (simplified)
        # Real ZIP codes have specific ranges
        first_digit = int(five_digit[0])
        
        # US ZIP codes start with specific ranges
        if first_digit == 0 and not five_digit.startswith("00"):
            result.add_warning("ZIP codes starting with 0 are typically in New England states.")
        elif first_digit > 9:
            result.add_error("Invalid ZIP code: first digit must be 0-9.")
    
    def _validate_geographic_ranges(self, zip_code: str, result: ValidationResult) -> None:
        """
        Validate ZIP code geographic ranges.
        
        Args:
            zip_code: ZIP code to validate
            result: ValidationResult to update
        """
        five_digit = self._extract_five_digit(zip_code)
        if not five_digit:
            return
        
        zip_int = int(five_digit)
        
        # Known invalid ranges
        if zip_int in range(0, 1000):  # 00000-00999
            result.add_error("Invalid ZIP code range: 00000-00999")
        elif zip_int in range(10000, 10010):  # 10000-10009 (reserved)
            result.add_warning("ZIP code range 10000-10009 is reserved.")
    
    def _extract_five_digit(self, zip_code: str) -> Optional[str]:
        """
        Extract 5-digit portion from ZIP code.
        
        Args:
            zip_code: ZIP code string
            
        Returns:
            5-digit string or None
        """
        # Remove spaces and dashes
        cleaned = re.sub(r'[-\s]', '', zip_code)
        
        # Return first 5 digits
        digits = re.findall(r'\d', cleaned)
        if len(digits) >= 5:
            return ''.join(digits[:5])
        
        return None
    
    def clean(self, data: str) -> str:
        """
        Clean and normalize ZIP code.
        
        Args:
            data: Raw ZIP code data
            
        Returns:
            Cleaned ZIP code string
        """
        # Remove extra whitespace
        cleaned = data.strip()
        
        # Remove invalid characters (keep only digits, letters, spaces, dashes)
        cleaned = re.sub(r'[^A-Za-z0-9\s-]', '', cleaned)
        
        # Normalize spaces and dashes
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single
        cleaned = re.sub(r'-+', '-', cleaned)   # Multiple dashes to single
        
        # Normalize format if specified
        if self.normalize_format:
            cleaned = self._normalize_format(cleaned, self.normalize_format)
        
        return cleaned
    
    def _normalize_format(self, zip_code: str, target_format: str) -> str:
        """
        Normalize ZIP code to target format.
        
        Args:
            zip_code: ZIP code to normalize
            target_format: Target format ("5", "5+4", "9")
            
        Returns:
            Normalized ZIP code
        """
        # Extract digits
        digits = re.findall(r'\d', zip_code)
        if len(digits) < 5:
            return zip_code  # Can't normalize
        
        five_digit = ''.join(digits[:5])
        
        if target_format == "5":
            return five_digit
        elif target_format == "5+4":
            if len(digits) >= 9:
                return f"{five_digit}-{''.join(digits[5:9])}"
            else:
                return five_digit
        elif target_format == "9":
            if len(digits) >= 9:
                return ''.join(digits[:9])
            else:
                return five_digit
        
        return zip_code
    
    def process(self, data: InputData) -> ProcessedData:
        """
        Process ZIP code through validation and cleaning.
        
        Args:
            data: InputData containing ZIP code
            
        Returns:
            ProcessedData with results
        """
        if data.input_type != InputType.ZIP_CODE:
            raise ProcessingError(f"Invalid input type {data.input_type} for ZipCodeHandler")
        
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
        
        # Extract format information
        detected_format = self._detect_format(cleaned_data)
        
        return ProcessedData(
            original_data=data.data,
            processed_data=cleaned_data,
            input_type=data.input_type,
            status=status,
            validation_result=validation_result,
            metadata={
                **data.metadata,
                "handler": "ZipCodeHandler",
                "config": self.config,
                "detected_format": detected_format,
                "five_digit_code": self._extract_five_digit(cleaned_data)
            },
            processing_timestamp=datetime.now().isoformat()
        )

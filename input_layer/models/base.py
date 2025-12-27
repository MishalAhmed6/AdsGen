"""
Base classes for Input Layer handlers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .input_types import InputData, ProcessedData, ValidationResult


class BaseHandler(ABC):
    """Abstract base class for all input handlers."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the handler with optional configuration.
        
        Args:
            config: Configuration dictionary for the handler
        """
        self.config = config or {}
    
    @abstractmethod
    def validate(self, data: InputData) -> ValidationResult:
        """
        Validate input data.
        
        Args:
            data: Input data to validate
            
        Returns:
            ValidationResult object with validation status and messages
        """
        pass
    
    @abstractmethod
    def clean(self, data: str) -> str:
        """
        Clean and normalize input data.
        
        Args:
            data: Raw input data
            
        Returns:
            Cleaned data string
        """
        pass
    
    @abstractmethod
    def process(self, data: InputData) -> ProcessedData:
        """
        Process input data through validation and cleaning.
        
        Args:
            data: Input data to process
            
        Returns:
            ProcessedData object with results
        """
        pass
    
    def batch_process(self, data_list: List[InputData]) -> List[ProcessedData]:
        """
        Process multiple input data items in batch.
        
        Args:
            data_list: List of InputData objects
            
        Returns:
            List of ProcessedData objects
        """
        results = []
        for data in data_list:
            try:
                result = self.process(data)
                results.append(result)
            except Exception as e:
                # Create a failed result for error handling
                failed_result = ProcessedData(
                    original_data=data.data,
                    processed_data="",
                    input_type=data.input_type,
                    status="failed",
                    validation_result=ValidationResult(is_valid=False),
                    metadata={"error": str(e)}
                )
                results.append(failed_result)
        
        return results

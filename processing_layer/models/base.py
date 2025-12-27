"""
Base classes for Processing Layer analyzers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..exceptions import AnalysisError


class BaseAnalyzer(ABC):
    """Abstract base class for all context analyzers."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the analyzer with optional configuration.
        
        Args:
            config: Configuration dictionary for the analyzer
        """
        self.config = config or {}
    
    @abstractmethod
    def analyze(self, data: Any) -> Any:
        """
        Perform analysis on the provided data.
        
        Args:
            data: Data to analyze
            
        Returns:
            Analysis result object
            
        Raises:
            AnalysisError: If analysis fails
        """
        pass
    
    def validate_input(self, data: Any) -> None:
        """
        Validate input data before analysis.
        
        Args:
            data: Data to validate
            
        Raises:
            AnalysisError: If data is invalid
        """
        if data is None:
            raise AnalysisError("Input data cannot be None")
    
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

"""
Processing Layer Module

A comprehensive marketing context analysis system that:
- Detects local tone and sentiment from competitor data
- Extracts keyword patterns from competitor names and hashtags
- Analyzes regional information from ZIP codes
- Builds structured context objects for AI generation

Features:
- Tone analysis and sentiment detection
- Keyword pattern extraction and categorization
- Regional demographic and geographic analysis
- Context aggregation and structuring
- Integration with Input Layer data
"""

from .core.processing_layer import ProcessingLayer
from .analyzers.tone_analyzer import ToneAnalyzer
from .analyzers.keyword_extractor import KeywordExtractor
from .analyzers.regional_analyzer import RegionalAnalyzer
from .models.context_types import MarketingContext, ToneAnalysis, KeywordPatterns, RegionalInfo
from .exceptions import ProcessingLayerError, AnalysisError, ContextBuildingError

__version__ = "1.0.0"
__all__ = [
    "ProcessingLayer",
    "ToneAnalyzer",
    "KeywordExtractor", 
    "RegionalAnalyzer",
    "MarketingContext",
    "ToneAnalysis",
    "KeywordPatterns",
    "RegionalInfo",
    "ProcessingLayerError",
    "AnalysisError",
    "ContextBuildingError"
]

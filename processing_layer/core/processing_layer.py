"""
Main Processing Layer orchestrator class.
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

from ..analyzers.tone_analyzer import ToneAnalyzer
from ..analyzers.keyword_extractor import KeywordExtractor
from ..analyzers.regional_analyzer import RegionalAnalyzer
from ..models.context_types import MarketingContext, ToneAnalysis, KeywordPatterns, RegionalInfo
from ..exceptions import ProcessingLayerError, ContextBuildingError


class ProcessingLayer:
    """
    Main orchestrator class for the Processing Layer module.
    
    This class coordinates the analysis of processed input data to build
    comprehensive marketing context including tone analysis, keyword patterns,
    and regional information.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Processing Layer with configuration.
        
        Args:
            config: Configuration dictionary with analyzer-specific configs:
                - tone_analyzer: Config for ToneAnalyzer
                - keyword_extractor: Config for KeywordExtractor
                - regional_analyzer: Config for RegionalAnalyzer
                - global_settings: Global settings for all analyzers
        """
        self.config = config or {}
        self.global_config = self.config.get("global_settings", {})
        
        # Initialize analyzers
        self.tone_analyzer = ToneAnalyzer(
            self.config.get("tone_analyzer", {})
        )
        self.keyword_extractor = KeywordExtractor(
            self.config.get("keyword_extractor", {})
        )
        self.regional_analyzer = RegionalAnalyzer(
            self.config.get("regional_analyzer", {})
        )
        
        # Processing statistics
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "analysis_breakdown": {
                "tone_analysis": {"processed": 0, "successful": 0, "failed": 0},
                "keyword_extraction": {"processed": 0, "successful": 0, "failed": 0},
                "regional_analysis": {"processed": 0, "successful": 0, "failed": 0}
            }
        }
    
    def build_context(self, processed_data: List[Dict[str, Any]]) -> MarketingContext:
        """
        Build comprehensive marketing context from processed input data.
        
        Args:
            processed_data: List of processed data from Input Layer
            
        Returns:
            MarketingContext object with complete analysis
            
        Raises:
            ContextBuildingError: If context building fails
        """
        if not processed_data:
            raise ContextBuildingError("No processed data provided")
        
        try:
            self.stats["total_processed"] += 1
            
            # Perform tone analysis
            tone_analysis = self._perform_tone_analysis(processed_data)
            
            # Extract keyword patterns
            keyword_patterns = self._perform_keyword_extraction(processed_data)
            
            # Analyze regional information
            regional_info = self._perform_regional_analysis(processed_data)
            
            # Calculate overall confidence score
            confidence_score = self._calculate_confidence_score(
                tone_analysis, keyword_patterns, regional_info
            )
            
            # Create marketing context
            context = MarketingContext(
                tone_analysis=tone_analysis,
                keyword_patterns=keyword_patterns,
                regional_info=regional_info,
                analysis_metadata={
                    "total_input_items": len(processed_data),
                    "input_types": list(set(item.get("input_type", "unknown") for item in processed_data)),
                    "processing_version": "1.0.0"
                },
                processing_timestamp=datetime.now().isoformat(),
                confidence_score=confidence_score
            )
            
            self.stats["successful"] += 1
            return context
            
        except Exception as e:
            self.stats["failed"] += 1
            raise ContextBuildingError(f"Failed to build marketing context: {str(e)}") from e
    
    def analyze_tone_only(self, processed_data: List[Dict[str, Any]]) -> ToneAnalysis:
        """
        Perform only tone analysis on processed data.
        
        Args:
            processed_data: List of processed data from Input Layer
            
        Returns:
            ToneAnalysis object
            
        Raises:
            ProcessingLayerError: If analysis fails
        """
        try:
            return self._perform_tone_analysis(processed_data)
        except Exception as e:
            raise ProcessingLayerError(f"Tone analysis failed: {str(e)}") from e
    
    def extract_keywords_only(self, processed_data: List[Dict[str, Any]]) -> KeywordPatterns:
        """
        Perform only keyword extraction on processed data.
        
        Args:
            processed_data: List of processed data from Input Layer
            
        Returns:
            KeywordPatterns object
            
        Raises:
            ProcessingLayerError: If extraction fails
        """
        try:
            return self._perform_keyword_extraction(processed_data)
        except Exception as e:
            raise ProcessingLayerError(f"Keyword extraction failed: {str(e)}") from e
    
    def analyze_regional_only(self, processed_data: List[Dict[str, Any]]) -> RegionalInfo:
        """
        Perform only regional analysis on processed data.
        
        Args:
            processed_data: List of processed data from Input Layer
            
        Returns:
            RegionalInfo object
            
        Raises:
            ProcessingLayerError: If analysis fails
        """
        try:
            return self._perform_regional_analysis(processed_data)
        except Exception as e:
            raise ProcessingLayerError(f"Regional analysis failed: {str(e)}") from e
    
    def _perform_tone_analysis(self, processed_data: List[Dict[str, Any]]) -> ToneAnalysis:
        """Perform tone analysis using ToneAnalyzer."""
        try:
            self.stats["analysis_breakdown"]["tone_analysis"]["processed"] += 1
            result = self.tone_analyzer.analyze(processed_data)
            self.stats["analysis_breakdown"]["tone_analysis"]["successful"] += 1
            return result
        except Exception as e:
            self.stats["analysis_breakdown"]["tone_analysis"]["failed"] += 1
            raise
    
    def _perform_keyword_extraction(self, processed_data: List[Dict[str, Any]]) -> KeywordPatterns:
        """Perform keyword extraction using KeywordExtractor."""
        try:
            self.stats["analysis_breakdown"]["keyword_extraction"]["processed"] += 1
            result = self.keyword_extractor.analyze(processed_data)
            self.stats["analysis_breakdown"]["keyword_extraction"]["successful"] += 1
            return result
        except Exception as e:
            self.stats["analysis_breakdown"]["keyword_extraction"]["failed"] += 1
            raise
    
    def _perform_regional_analysis(self, processed_data: List[Dict[str, Any]]) -> RegionalInfo:
        """Perform regional analysis using RegionalAnalyzer."""
        try:
            self.stats["analysis_breakdown"]["regional_analysis"]["processed"] += 1
            result = self.regional_analyzer.analyze(processed_data)
            self.stats["analysis_breakdown"]["regional_analysis"]["successful"] += 1
            return result
        except Exception as e:
            self.stats["analysis_breakdown"]["regional_analysis"]["failed"] += 1
            raise
    
    def _calculate_confidence_score(self, tone_analysis: ToneAnalysis,
                                  keyword_patterns: KeywordPatterns,
                                  regional_info: RegionalInfo) -> float:
        """Calculate overall confidence score for the analysis."""
        scores = []
        
        # Tone analysis confidence
        scores.append(tone_analysis.confidence)
        
        # Keyword extraction confidence (based on number of keywords found)
        total_keywords = len(keyword_patterns.get_all_keywords())
        keyword_confidence = min(total_keywords / 10.0, 1.0)  # Normalize to 0-1
        scores.append(keyword_confidence)
        
        # Regional analysis confidence (based on completeness)
        regional_confidence = 0.0
        if regional_info.primary_region:
            regional_confidence += 0.4
        if regional_info.state:
            regional_confidence += 0.3
        if regional_info.metro_area:
            regional_confidence += 0.3
        scores.append(regional_confidence)
        
        # Return average confidence
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with processing statistics
        """
        return {
            "statistics": self.stats.copy(),
            "success_rate": (
                self.stats["successful"] / self.stats["total_processed"] * 100
                if self.stats["total_processed"] > 0 else 0
            ),
            "last_updated": datetime.now().isoformat()
        }
    
    def reset_statistics(self) -> None:
        """Reset processing statistics."""
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "analysis_breakdown": {
                "tone_analysis": {"processed": 0, "successful": 0, "failed": 0},
                "keyword_extraction": {"processed": 0, "successful": 0, "failed": 0},
                "regional_analysis": {"processed": 0, "successful": 0, "failed": 0}
            }
        }
    
    def export_context(self, context: MarketingContext, format: str = "json") -> str:
        """
        Export marketing context to specified format.
        
        Args:
            context: MarketingContext object to export
            format: Export format ("json", "summary")
            
        Returns:
            Exported data as string
            
        Raises:
            ProcessingLayerError: If format is not supported
        """
        if format == "json":
            return json.dumps(context.to_dict(), indent=2)
        elif format == "summary":
            return self._generate_summary_report(context)
        else:
            raise ProcessingLayerError(f"Unsupported export format: {format}")
    
    def _generate_summary_report(self, context: MarketingContext) -> str:
        """Generate a human-readable summary report."""
        report = []
        report.append("=== Marketing Context Analysis Report ===\n")
        
        # Tone Analysis Summary
        report.append("TONE ANALYSIS:")
        report.append(f"  Primary Tone: {context.tone_analysis.primary_tone.value}")
        if context.tone_analysis.secondary_tones:
            secondary = ", ".join([t.value for t in context.tone_analysis.secondary_tones])
            report.append(f"  Secondary Tones: {secondary}")
        report.append(f"  Sentiment: {context.tone_analysis.sentiment.value}")
        report.append(f"  Confidence: {context.tone_analysis.confidence:.2f}")
        
        if context.tone_analysis.local_indicators:
            report.append(f"  Local Indicators: {', '.join(context.tone_analysis.local_indicators)}")
        
        if context.tone_analysis.corporate_indicators:
            report.append(f"  Corporate Indicators: {', '.join(context.tone_analysis.corporate_indicators)}")
        
        report.append("")
        
        # Keyword Patterns Summary
        report.append("KEYWORD PATTERNS:")
        total_keywords = len(context.keyword_patterns.get_all_keywords())
        report.append(f"  Total Keywords: {total_keywords}")
        
        if context.keyword_patterns.industry_keywords:
            report.append(f"  Industries: {', '.join(context.keyword_patterns.industry_keywords)}")
        
        if context.keyword_patterns.technology_keywords:
            report.append(f"  Technologies: {', '.join(context.keyword_patterns.technology_keywords)}")
        
        if context.keyword_patterns.common_patterns:
            report.append(f"  Common Patterns: {', '.join(context.keyword_patterns.common_patterns[:5])}")  # Top 5
        
        report.append("")
        
        # Regional Information Summary
        report.append("REGIONAL INFORMATION:")
        if context.regional_info.primary_region:
            report.append(f"  Primary Region: {context.regional_info.primary_region}")
        
        if context.regional_info.region_type:
            report.append(f"  Region Type: {context.regional_info.region_type.value}")
        
        if context.regional_info.state:
            report.append(f"  State: {context.regional_info.state}")
        
        if context.regional_info.metro_area:
            report.append(f"  Metro Area: {context.regional_info.metro_area}")
        
        if context.regional_info.population_density:
            report.append(f"  Population Density: {context.regional_info.population_density}")
        
        if context.regional_info.market_characteristics:
            report.append(f"  Market Characteristics: {', '.join(context.regional_info.market_characteristics[:5])}")  # Top 5
        
        report.append("")
        
        # Overall Summary
        report.append("OVERALL ANALYSIS:")
        report.append(f"  Confidence Score: {context.confidence_score:.2f}")
        report.append(f"  Processing Timestamp: {context.processing_timestamp}")
        
        return "\n".join(report)
    
    def get_analyzer_config(self, analyzer_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific analyzer.
        
        Args:
            analyzer_name: Name of the analyzer ("tone_analyzer", "keyword_extractor", "regional_analyzer")
            
        Returns:
            Analyzer configuration dictionary
            
        Raises:
            ProcessingLayerError: If analyzer name is not supported
        """
        analyzer_mapping = {
            "tone_analyzer": self.tone_analyzer.config,
            "keyword_extractor": self.keyword_extractor.config,
            "regional_analyzer": self.regional_analyzer.config
        }
        
        if analyzer_name not in analyzer_mapping:
            raise ProcessingLayerError(f"Unknown analyzer: {analyzer_name}")
        
        return analyzer_mapping[analyzer_name]
    
    def update_analyzer_config(self, analyzer_name: str, config: Dict[str, Any]) -> None:
        """
        Update configuration for a specific analyzer.
        
        Args:
            analyzer_name: Name of the analyzer to update
            config: New configuration dictionary
            
        Raises:
            ProcessingLayerError: If analyzer name is not supported
        """
        if analyzer_name == "tone_analyzer":
            self.tone_analyzer.config.update(config)
            self.tone_analyzer = ToneAnalyzer(self.tone_analyzer.config)
        elif analyzer_name == "keyword_extractor":
            self.keyword_extractor.config.update(config)
            self.keyword_extractor = KeywordExtractor(self.keyword_extractor.config)
        elif analyzer_name == "regional_analyzer":
            self.regional_analyzer.config.update(config)
            self.regional_analyzer = RegionalAnalyzer(self.regional_analyzer.config)
        else:
            raise ProcessingLayerError(f"Unknown analyzer: {analyzer_name}")

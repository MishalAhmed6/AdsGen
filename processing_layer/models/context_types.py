"""
Data type definitions for Processing Layer context analysis.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class ToneType(Enum):
    """Types of tone detected."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FORMAL = "formal"
    PLAYFUL = "playful"
    TECHNICAL = "technical"
    LOCAL = "local"
    CORPORATE = "corporate"


class SentimentType(Enum):
    """Sentiment classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class KeywordCategory(Enum):
    """Categories for extracted keywords."""
    INDUSTRY = "industry"
    TECHNOLOGY = "technology"
    BUSINESS_TYPE = "business_type"
    LOCATION = "location"
    BRAND_ATTRIBUTE = "brand_attribute"
    PRODUCT_SERVICE = "product_service"
    TREND = "trend"


class RegionType(Enum):
    """Types of regional classifications."""
    URBAN = "urban"
    SUBURBAN = "suburban"
    RURAL = "rural"
    METROPOLITAN = "metropolitan"


@dataclass
class ToneAnalysis:
    """Results of tone analysis."""
    primary_tone: ToneType
    secondary_tones: List[ToneType] = field(default_factory=list)
    sentiment: SentimentType = SentimentType.NEUTRAL
    confidence: float = 0.0
    local_indicators: List[str] = field(default_factory=list)
    corporate_indicators: List[str] = field(default_factory=list)
    technical_terms: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "primary_tone": self.primary_tone.value,
            "secondary_tones": [tone.value for tone in self.secondary_tones],
            "sentiment": self.sentiment.value,
            "confidence": self.confidence,
            "local_indicators": self.local_indicators,
            "corporate_indicators": self.corporate_indicators,
            "technical_terms": self.technical_terms
        }


@dataclass
class KeywordPatterns:
    """Extracted keyword patterns and categorization."""
    industry_keywords: List[str] = field(default_factory=list)
    technology_keywords: List[str] = field(default_factory=list)
    business_type_keywords: List[str] = field(default_factory=list)
    location_keywords: List[str] = field(default_factory=list)
    brand_attribute_keywords: List[str] = field(default_factory=list)
    product_service_keywords: List[str] = field(default_factory=list)
    trend_keywords: List[str] = field(default_factory=list)
    common_patterns: List[str] = field(default_factory=list)
    unique_patterns: List[str] = field(default_factory=list)
    frequency_map: Dict[str, int] = field(default_factory=dict)
    
    def get_all_keywords(self) -> List[str]:
        """Get all keywords across all categories."""
        all_keywords = []
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, list) and field_name != "common_patterns" and field_name != "unique_patterns":
                all_keywords.extend(field_value)
        return list(set(all_keywords))  # Remove duplicates
    
    def get_category_keywords(self, category: KeywordCategory) -> List[str]:
        """Get keywords for a specific category."""
        category_mapping = {
            KeywordCategory.INDUSTRY: self.industry_keywords,
            KeywordCategory.TECHNOLOGY: self.technology_keywords,
            KeywordCategory.BUSINESS_TYPE: self.business_type_keywords,
            KeywordCategory.LOCATION: self.location_keywords,
            KeywordCategory.BRAND_ATTRIBUTE: self.brand_attribute_keywords,
            KeywordCategory.PRODUCT_SERVICE: self.product_service_keywords,
            KeywordCategory.TREND: self.trend_keywords
        }
        return category_mapping.get(category, [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "industry_keywords": self.industry_keywords,
            "technology_keywords": self.technology_keywords,
            "business_type_keywords": self.business_type_keywords,
            "location_keywords": self.location_keywords,
            "brand_attribute_keywords": self.brand_attribute_keywords,
            "product_service_keywords": self.product_service_keywords,
            "trend_keywords": self.trend_keywords,
            "common_patterns": self.common_patterns,
            "unique_patterns": self.unique_patterns,
            "frequency_map": self.frequency_map
        }


@dataclass
class RegionalInfo:
    """Regional information derived from ZIP codes."""
    primary_region: Optional[str] = None
    region_type: Optional[RegionType] = None
    state: Optional[str] = None
    metro_area: Optional[str] = None
    population_density: Optional[str] = None
    economic_indicators: Dict[str, Any] = field(default_factory=dict)
    demographic_indicators: Dict[str, Any] = field(default_factory=dict)
    geographic_features: List[str] = field(default_factory=list)
    market_characteristics: List[str] = field(default_factory=list)
    zip_codes_analyzed: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "primary_region": self.primary_region,
            "region_type": self.region_type.value if self.region_type else None,
            "state": self.state,
            "metro_area": self.metro_area,
            "population_density": self.population_density,
            "economic_indicators": self.economic_indicators,
            "demographic_indicators": self.demographic_indicators,
            "geographic_features": self.geographic_features,
            "market_characteristics": self.market_characteristics,
            "zip_codes_analyzed": self.zip_codes_analyzed
        }


@dataclass
class MarketingContext:
    """Complete marketing context analysis result."""
    tone_analysis: ToneAnalysis
    keyword_patterns: KeywordPatterns
    regional_info: RegionalInfo
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)
    processing_timestamp: Optional[str] = None
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for AI generation."""
        return {
            "tone_analysis": self.tone_analysis.to_dict(),
            "keyword_patterns": self.keyword_patterns.to_dict(),
            "regional_info": self.regional_info.to_dict(),
            "analysis_metadata": self.analysis_metadata,
            "processing_timestamp": self.processing_timestamp,
            "confidence_score": self.confidence_score,
            "summary": self.generate_summary()
        }
    
    def generate_summary(self) -> str:
        """Generate a human-readable summary of the context."""
        summary_parts = []
        
        # Tone summary
        tone_summary = f"Primary tone: {self.tone_analysis.primary_tone.value}"
        if self.tone_analysis.secondary_tones:
            secondary = ", ".join([t.value for t in self.tone_analysis.secondary_tones])
            tone_summary += f" (with {secondary} elements)"
        summary_parts.append(tone_summary)
        
        # Keyword summary
        total_keywords = len(self.keyword_patterns.get_all_keywords())
        top_categories = []
        for category in [KeywordCategory.INDUSTRY, KeywordCategory.TECHNOLOGY, KeywordCategory.BUSINESS_TYPE]:
            keywords = self.keyword_patterns.get_category_keywords(category)
            if keywords:
                top_categories.append(f"{category.value}: {len(keywords)} keywords")
        
        if top_categories:
            summary_parts.append(f"Keywords identified: {total_keywords} total ({', '.join(top_categories)})")
        
        # Regional summary
        if self.regional_info.primary_region:
            region_summary = f"Target region: {self.regional_info.primary_region}"
            if self.regional_info.region_type:
                region_summary += f" ({self.regional_info.region_type.value})"
            summary_parts.append(region_summary)
        
        return ". ".join(summary_parts) + "."

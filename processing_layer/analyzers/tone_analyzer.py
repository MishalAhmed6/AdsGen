"""
Tone analyzer for detecting local tone and sentiment from competitor data.
"""

import re
from typing import List, Dict, Any, Set, Tuple
from collections import Counter
from datetime import datetime

from ..models.base import BaseAnalyzer
from ..models.context_types import ToneAnalysis, ToneType, SentimentType
from ..exceptions import ToneAnalysisError


class ToneAnalyzer(BaseAnalyzer):
    """Analyzer for detecting tone and sentiment from competitor data."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize tone analyzer with configuration.
        
        Args:
            config: Configuration dictionary with options:
                - local_indicators: List of local business indicators
                - corporate_indicators: List of corporate business indicators
                - technical_terms: List of technical terms
                - sentiment_words: Dictionary of sentiment word mappings
                - tone_weights: Weights for different tone factors
        """
        super().__init__(config)
        
        # Load tone indicators from config or use defaults
        self.local_indicators = set(self.get_config_value("local_indicators", [
            "local", "family", "community", "neighborhood", "hometown", "mom", "pop",
            "corner", "shop", "store", "market", "cafe", "diner", "pizzeria",
            "boutique", "studio", "salon", "clinic", "pharmacy", "bakery",
            "fresh", "handmade", "artisan", "craft", "traditional", "authentic"
        ]))
        
        self.corporate_indicators = set(self.get_config_value("corporate_indicators", [
            "corporation", "corp", "inc", "llc", "ltd", "company", "enterprise",
            "global", "international", "worldwide", "national", "systems",
            "solutions", "services", "group", "holdings", "ventures",
            "technologies", "digital", "software", "consulting", "management"
        ]))
        
        self.technical_terms = set(self.get_config_value("technical_terms", [
            "software", "technology", "digital", "cloud", "data", "analytics",
            "platform", "solution", "system", "api", "mobile", "web",
            "development", "engineering", "innovation", "automation",
            "artificial", "intelligence", "machine", "learning", "blockchain"
        ]))
        
        # Sentiment analysis words
        self.sentiment_words = self.get_config_value("sentiment_words", {
            "positive": ["excellent", "amazing", "great", "best", "top", "premium", 
                        "quality", "reliable", "trusted", "innovative", "cutting-edge"],
            "negative": ["cheap", "poor", "worst", "bad", "terrible", "awful", 
                        "unreliable", "outdated", "broken", "failed", "disappointing"]
        })
        
        # Tone detection weights
        self.tone_weights = self.get_config_value("tone_weights", {
            "local_indicators": 0.4,
            "corporate_indicators": 0.3,
            "technical_terms": 0.2,
            "length_factor": 0.1
        })
    
    def analyze(self, data: List[Dict[str, Any]]) -> ToneAnalysis:
        """
        Analyze tone and sentiment from processed input data.
        
        Args:
            data: List of processed data from Input Layer
            
        Returns:
            ToneAnalysis object with detected tone and sentiment
            
        Raises:
            ToneAnalysisError: If analysis fails
        """
        self.validate_input(data)
        
        try:
            # Extract text from different input types
            competitor_texts = []
            hashtag_texts = []
            
            for item in data:
                if item.get("input_type") == "competitor_name":
                    competitor_texts.append(item.get("processed_data", ""))
                elif item.get("input_type") == "hashtag":
                    hashtag_texts.append(item.get("processed_data", ""))
            
            # Combine all text for analysis
            all_text = " ".join(competitor_texts + hashtag_texts).lower()
            
            # Analyze tone components
            local_score, local_found = self._analyze_local_indicators(all_text)
            corporate_score, corporate_found = self._analyze_corporate_indicators(all_text)
            technical_score, technical_found = self._analyze_technical_terms(all_text)
            
            # Determine primary tone
            primary_tone = self._determine_primary_tone(
                local_score, corporate_score, technical_score
            )
            
            # Determine secondary tones
            secondary_tones = self._determine_secondary_tones(
                local_score, corporate_score, technical_score, primary_tone
            )
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment(all_text)
            
            # Calculate confidence
            confidence = self._calculate_confidence(
                local_score, corporate_score, technical_score
            )
            
            return ToneAnalysis(
                primary_tone=primary_tone,
                secondary_tones=secondary_tones,
                sentiment=sentiment,
                confidence=confidence,
                local_indicators=list(local_found),
                corporate_indicators=list(corporate_found),
                technical_terms=list(technical_found)
            )
            
        except Exception as e:
            raise ToneAnalysisError(f"Tone analysis failed: {str(e)}") from e
    
    def _analyze_local_indicators(self, text: str) -> Tuple[float, Set[str]]:
        """Analyze local business indicators in text."""
        found_indicators = set()
        
        for indicator in self.local_indicators:
            if re.search(r'\b' + re.escape(indicator) + r'\b', text):
                found_indicators.add(indicator)
        
        score = len(found_indicators) / len(self.local_indicators) if self.local_indicators else 0
        return score, found_indicators
    
    def _analyze_corporate_indicators(self, text: str) -> Tuple[float, Set[str]]:
        """Analyze corporate business indicators in text."""
        found_indicators = set()
        
        for indicator in self.corporate_indicators:
            if re.search(r'\b' + re.escape(indicator) + r'\b', text):
                found_indicators.add(indicator)
        
        score = len(found_indicators) / len(self.corporate_indicators) if self.corporate_indicators else 0
        return score, found_indicators
    
    def _analyze_technical_terms(self, text: str) -> Tuple[float, Set[str]]:
        """Analyze technical terms in text."""
        found_terms = set()
        
        for term in self.technical_terms:
            if re.search(r'\b' + re.escape(term) + r'\b', text):
                found_terms.add(term)
        
        score = len(found_terms) / len(self.technical_terms) if self.technical_terms else 0
        return score, found_terms
    
    def _determine_primary_tone(self, local_score: float, corporate_score: float, 
                              technical_score: float) -> ToneType:
        """Determine the primary tone based on scores."""
        scores = {
            ToneType.LOCAL: local_score * self.tone_weights["local_indicators"],
            ToneType.CORPORATE: corporate_score * self.tone_weights["corporate_indicators"],
            ToneType.TECHNICAL: technical_score * self.tone_weights["technical_terms"]
        }
        
        # Find the tone with the highest score
        max_tone, max_score = max(scores.items(), key=lambda x: x[1])
        
        # Default to professional if no strong indicators (score < 0.05)
        if max_score < 0.05:
            return ToneType.PROFESSIONAL
        
        return max_tone
    
    def _determine_secondary_tones(self, local_score: float, corporate_score: float,
                                 technical_score: float, primary_tone: ToneType) -> List[ToneType]:
        """Determine secondary tones based on scores."""
        secondary_tones = []
        
        # Add tones with significant scores that aren't primary
        if local_score > 0.2 and primary_tone != ToneType.LOCAL:
            secondary_tones.append(ToneType.LOCAL)
        
        if corporate_score > 0.2 and primary_tone != ToneType.CORPORATE:
            secondary_tones.append(ToneType.CORPORATE)
        
        if technical_score > 0.2 and primary_tone != ToneType.TECHNICAL:
            secondary_tones.append(ToneType.TECHNICAL)
        
        # Add casual tone if local indicators are present
        if local_score > 0.1:
            secondary_tones.append(ToneType.CASUAL)
        
        # Add formal tone if corporate indicators are strong
        if corporate_score > 0.3:
            secondary_tones.append(ToneType.FORMAL)
        
        return list(set(secondary_tones))  # Remove duplicates
    
    def _analyze_sentiment(self, text: str) -> SentimentType:
        """Analyze sentiment from text."""
        positive_count = 0
        negative_count = 0
        
        for word in self.sentiment_words.get("positive", []):
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                positive_count += 1
        
        for word in self.sentiment_words.get("negative", []):
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                negative_count += 1
        
        # Determine sentiment
        if positive_count > negative_count:
            return SentimentType.POSITIVE
        elif negative_count > positive_count:
            return SentimentType.NEGATIVE
        elif positive_count > 0 and negative_count > 0:
            return SentimentType.MIXED
        else:
            return SentimentType.NEUTRAL
    
    def _calculate_confidence(self, local_score: float, corporate_score: float,
                            technical_score: float) -> float:
        """Calculate confidence score for the tone analysis."""
        # Base confidence on the strength of indicators
        max_score = max(local_score, corporate_score, technical_score)
        
        # Boost confidence if multiple indicators align
        total_indicators = sum([
            local_score > 0.1,
            corporate_score > 0.1,
            technical_score > 0.1
        ])
        
        alignment_bonus = min(total_indicators * 0.1, 0.3)
        
        return min(max_score + alignment_bonus, 1.0)

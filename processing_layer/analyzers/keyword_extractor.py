"""
Keyword pattern extractor for analyzing competitor names and hashtags.
"""

import re
from typing import List, Dict, Any, Set, Tuple
from collections import Counter
from datetime import datetime

from ..models.base import BaseAnalyzer
from ..models.context_types import KeywordPatterns, KeywordCategory
from ..exceptions import KeywordExtractionError


class KeywordExtractor(BaseAnalyzer):
    """Extractor for keyword patterns from competitor data."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize keyword extractor with configuration.
        
        Args:
            config: Configuration dictionary with options:
                - industry_keywords: Dictionary of industry keyword mappings
                - technology_keywords: List of technology-related keywords
                - business_type_keywords: Dictionary of business type keywords
                - location_keywords: List of location-related keywords
                - brand_attribute_keywords: Dictionary of brand attribute keywords
                - min_frequency: Minimum frequency for pattern detection
                - enable_stemming: Whether to use word stemming
        """
        super().__init__(config)
        
        # Industry keyword mappings
        self.industry_keywords = self.get_config_value("industry_keywords", {
            "technology": ["tech", "software", "digital", "computer", "internet", "web", "mobile", "app"],
            "healthcare": ["health", "medical", "clinic", "hospital", "pharmacy", "dental", "wellness"],
            "finance": ["bank", "financial", "credit", "loan", "investment", "insurance", "trading"],
            "retail": ["store", "shop", "market", "boutique", "fashion", "clothing", "retail"],
            "food": ["restaurant", "cafe", "food", "catering", "bakery", "pizza", "coffee"],
            "automotive": ["auto", "car", "vehicle", "garage", "repair", "dealer", "motor"],
            "real_estate": ["realty", "property", "homes", "construction", "building", "development"],
            "education": [
                "school", "education", "learning", "academy", "university", "training",
                "teacher", "teachers", "educator", "educators", "teaching", "classroom",
                "curriculum", "k12", "k-12", "stem", "tutoring", "tutor", "student",
                "edtech", "educationtechnology", "campus"
            ],
            "beauty": ["beauty", "salon", "spa", "cosmetic", "hair", "nail", "skincare"],
            "fitness": ["fitness", "gym", "workout", "training", "sports", "health", "wellness"]
        })
        
        # Technology keywords
        self.technology_keywords = self.get_config_value("technology_keywords", [
            "software", "app", "platform", "cloud", "data", "analytics", "ai", "machine learning",
            "blockchain", "cyber", "security", "automation", "robotics", "iot", "api",
            "mobile", "web", "digital", "tech", "innovation", "solution", "system"
        ])
        
        # Business type keywords
        self.business_type_keywords = self.get_config_value("business_type_keywords", {
            "corporation": ["corp", "corporation", "inc", "incorporated", "company"],
            "llc": ["llc", "limited liability", "ltd"],
            "partnership": ["partners", "partnership", "associates"],
            "solo": ["solo", "individual", "personal", "private"],
            "franchise": ["franchise", "chain", "brand"],
            "consulting": ["consulting", "consultants", "advisors", "services"],
            "agency": ["agency", "bureau", "office", "group"]
        })
        
        # Location keywords
        self.location_keywords = self.get_config_value("location_keywords", [
            "local", "regional", "national", "global", "international", "worldwide",
            "city", "town", "village", "county", "state", "country", "metro",
            "downtown", "uptown", "suburb", "rural", "urban", "coastal", "mountain"
        ])
        
        # Brand attribute keywords
        self.brand_attribute_keywords = self.get_config_value("brand_attribute_keywords", {
            "premium": ["premium", "luxury", "high-end", "exclusive", "elite", "premium"],
            "affordable": ["affordable", "budget", "cheap", "economical", "value", "discount"],
            "quality": ["quality", "reliable", "trusted", "professional", "expert", "certified"],
            "innovative": ["innovative", "cutting-edge", "advanced", "modern", "next-gen"],
            "traditional": ["traditional", "classic", "established", "heritage", "authentic"],
            "family": ["family", "friendly", "welcoming", "personal", "caring", "supportive"]
        })
        
        # Configuration options
        self.min_frequency = self.get_config_value("min_frequency", 1)
        self.enable_stemming = self.get_config_value("enable_stemming", False)
        
        # Compile regex patterns for better performance
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns for keyword extraction."""
        # Pattern for extracting words (letters, numbers, and common business characters)
        self.word_pattern = re.compile(r'\b[a-zA-Z0-9&.-]+\b')
        
        # Pattern for hashtags
        self.hashtag_pattern = re.compile(r'#([a-zA-Z0-9_]+)')
        
        # Pattern for business suffixes
        self.business_suffix_pattern = re.compile(r'\b(corp|inc|llc|ltd|co|company|group|systems|solutions|services|technologies|enterprise|holdings|ventures|partners|associates)\b', re.IGNORECASE)
    
    def analyze(self, data: List[Dict[str, Any]]) -> KeywordPatterns:
        """
        Extract keyword patterns from processed input data.
        
        Args:
            data: List of processed data from Input Layer
            
        Returns:
            KeywordPatterns object with extracted keywords
            
        Raises:
            KeywordExtractionError: If extraction fails
        """
        self.validate_input(data)
        
        try:
            # Separate data by type
            competitor_names = []
            hashtags = []
            
            for item in data:
                if item.get("input_type") == "competitor_name":
                    competitor_names.append(item.get("processed_data", ""))
                elif item.get("input_type") == "hashtag":
                    hashtags.append(item.get("processed_data", ""))
            
            # Extract keywords from each type
            competitor_keywords = self._extract_from_competitor_names(competitor_names)
            hashtag_keywords = self._extract_from_hashtags(hashtags)
            
            # Combine and categorize all keywords
            all_keywords = competitor_keywords + hashtag_keywords
            
            # Categorize keywords
            categorized_keywords = self._categorize_keywords(all_keywords)
            
            # Find patterns
            patterns = self._find_patterns(all_keywords)
            
            # Create frequency map
            frequency_map = dict(Counter(all_keywords))
            
            return KeywordPatterns(
                industry_keywords=categorized_keywords.get("industry", []),
                technology_keywords=categorized_keywords.get("technology", []),
                business_type_keywords=categorized_keywords.get("business_type", []),
                location_keywords=categorized_keywords.get("location", []),
                brand_attribute_keywords=categorized_keywords.get("brand_attribute", []),
                product_service_keywords=categorized_keywords.get("product_service", []),
                trend_keywords=categorized_keywords.get("trend", []),
                common_patterns=patterns.get("common", []),
                unique_patterns=patterns.get("unique", []),
                frequency_map=frequency_map
            )
            
        except Exception as e:
            raise KeywordExtractionError(f"Keyword extraction failed: {str(e)}") from e
    
    def _extract_from_competitor_names(self, names: List[str]) -> List[str]:
        """Extract keywords from competitor names."""
        keywords = []
        
        for name in names:
            # Extract individual words
            words = self.word_pattern.findall(name.lower())
            
            # Filter out common business words that don't add value
            filtered_words = self._filter_business_words(words)
            
            keywords.extend(filtered_words)
        
        return keywords
    
    def _extract_from_hashtags(self, hashtags: List[str]) -> List[str]:
        """Extract keywords from hashtags."""
        keywords = []
        
        for hashtag_text in hashtags:
            # Extract hashtags
            hashtag_matches = self.hashtag_pattern.findall(hashtag_text.lower())
            
            # Extract words from hashtag content
            for hashtag in hashtag_matches:
                # Split compound hashtags (e.g., "digitalmarketing" -> ["digital", "marketing"])
                words = self._split_compound_hashtag(hashtag)
                keywords.extend(words)
        
        return keywords
    
    def _filter_business_words(self, words: List[str]) -> List[str]:
        """Filter out common business words that don't add analytical value."""
        common_business_words = {
            "the", "and", "of", "for", "with", "by", "at", "in", "on", "to", "from",
            "corp", "inc", "llc", "ltd", "company", "co", "group", "systems",
            "solutions", "services", "technologies", "enterprise"
        }
        
        return [word for word in words if word not in common_business_words and len(word) > 2]
    
    def _split_compound_hashtag(self, hashtag: str) -> List[str]:
        """Split compound hashtags into individual words."""
        # Common word boundaries in hashtags
        words = []
        
        # Try to split on common patterns
        # Split on capital letters (camelCase)
        if re.search(r'[A-Z]', hashtag):
            parts = re.split(r'(?=[A-Z])', hashtag)
            words.extend([part.lower() for part in parts if part])
        
        # Split on numbers
        elif re.search(r'\d', hashtag):
            parts = re.split(r'(\d+)', hashtag)
            words.extend([part.lower() for part in parts if part and not part.isdigit()])
        
        # If no clear splitting pattern, treat as single word
        else:
            words.append(hashtag)
        
        return words
    
    def _categorize_keywords(self, keywords: List[str]) -> Dict[str, List[str]]:
        """Categorize keywords into different types."""
        categorized = {
            "industry": [],
            "technology": [],
            "business_type": [],
            "location": [],
            "brand_attribute": [],
            "product_service": [],
            "trend": []
        }
        
        keyword_set = set(keywords)
        
        # Categorize industry keywords
        for industry, industry_words in self.industry_keywords.items():
            for word in industry_words:
                if word in keyword_set:
                    categorized["industry"].append(industry)
                    break
        
        # Categorize technology keywords
        for tech_word in self.technology_keywords:
            if tech_word in keyword_set:
                categorized["technology"].append(tech_word)
        
        # Categorize business type keywords
        for business_type, type_words in self.business_type_keywords.items():
            for word in type_words:
                if word in keyword_set:
                    categorized["business_type"].append(business_type)
                    break
        
        # Categorize location keywords
        for location_word in self.location_keywords:
            if location_word in keyword_set:
                categorized["location"].append(location_word)
        
        # Categorize brand attribute keywords
        for attribute, attr_words in self.brand_attribute_keywords.items():
            for word in attr_words:
                if word in keyword_set:
                    categorized["brand_attribute"].append(attribute)
                    break
        
        # Remove duplicates
        for category in categorized:
            categorized[category] = list(set(categorized[category]))
        
        return categorized
    
    def _find_patterns(self, keywords: List[str]) -> Dict[str, List[str]]:
        """Find common and unique patterns in keywords."""
        keyword_counter = Counter(keywords)
        
        # Find common patterns (appearing multiple times)
        common_patterns = [
            keyword for keyword, count in keyword_counter.items()
            if count >= self.min_frequency + 1
        ]
        
        # Find unique patterns (appearing only once)
        unique_patterns = [
            keyword for keyword, count in keyword_counter.items()
            if count == 1
        ]
        
        return {
            "common": common_patterns,
            "unique": unique_patterns
        }

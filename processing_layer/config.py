"""
Configuration utilities for the Processing Layer module.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path

from .exceptions import ProcessingLayerError


class ProcessingConfigManager:
    """Manager for Processing Layer configuration."""
    
    DEFAULT_CONFIG = {
        "tone_analyzer": {
            "local_indicators": [
                "local", "family", "community", "neighborhood", "hometown", "mom", "pop",
                "corner", "shop", "store", "market", "cafe", "diner", "pizzeria",
                "boutique", "studio", "salon", "clinic", "pharmacy", "bakery",
                "fresh", "handmade", "artisan", "craft", "traditional", "authentic"
            ],
            "corporate_indicators": [
                "corporation", "corp", "inc", "llc", "ltd", "company", "enterprise",
                "global", "international", "worldwide", "national", "systems",
                "solutions", "services", "group", "holdings", "ventures",
                "technologies", "digital", "software", "consulting", "management"
            ],
            "technical_terms": [
                "software", "technology", "digital", "cloud", "data", "analytics",
                "platform", "solution", "system", "api", "mobile", "web",
                "development", "engineering", "innovation", "automation",
                "artificial", "intelligence", "machine", "learning", "blockchain"
            ],
            "sentiment_words": {
                "positive": ["excellent", "amazing", "great", "best", "top", "premium", 
                            "quality", "reliable", "trusted", "innovative", "cutting-edge"],
                "negative": ["cheap", "poor", "worst", "bad", "terrible", "awful", 
                            "unreliable", "outdated", "broken", "failed", "disappointing"]
            },
            "tone_weights": {
                "local_indicators": 0.4,
                "corporate_indicators": 0.3,
                "technical_terms": 0.2,
                "length_factor": 0.1
            }
        },
        "keyword_extractor": {
            "industry_keywords": {
                "technology": ["tech", "software", "digital", "computer", "internet", "web", "mobile", "app"],
                "healthcare": ["health", "medical", "clinic", "hospital", "pharmacy", "dental", "wellness"],
                "finance": ["bank", "financial", "credit", "loan", "investment", "insurance", "trading"],
                "retail": ["store", "shop", "market", "boutique", "fashion", "clothing", "retail"],
                "food": ["restaurant", "cafe", "food", "catering", "bakery", "pizza", "coffee"],
                "automotive": ["auto", "car", "vehicle", "garage", "repair", "dealer", "motor"],
                "real_estate": ["realty", "property", "homes", "construction", "building", "development"],
                "education": ["school", "education", "learning", "academy", "university", "training"],
                "beauty": ["beauty", "salon", "spa", "cosmetic", "hair", "nail", "skincare"],
                "fitness": ["fitness", "gym", "workout", "training", "sports", "health", "wellness"]
            },
            "technology_keywords": [
                "software", "app", "platform", "cloud", "data", "analytics", "ai", "machine learning",
                "blockchain", "cyber", "security", "automation", "robotics", "iot", "api",
                "mobile", "web", "digital", "tech", "innovation", "solution", "system"
            ],
            "business_type_keywords": {
                "corporation": ["corp", "corporation", "inc", "incorporated", "company"],
                "llc": ["llc", "limited liability", "ltd"],
                "partnership": ["partners", "partnership", "associates"],
                "solo": ["solo", "individual", "personal", "private"],
                "franchise": ["franchise", "chain", "brand"],
                "consulting": ["consulting", "consultants", "advisors", "services"],
                "agency": ["agency", "bureau", "office", "group"]
            },
            "location_keywords": [
                "local", "regional", "national", "global", "international", "worldwide",
                "city", "town", "village", "county", "state", "country", "metro",
                "downtown", "uptown", "suburb", "rural", "urban", "coastal", "mountain"
            ],
            "brand_attribute_keywords": {
                "premium": ["premium", "luxury", "high-end", "exclusive", "elite", "premium"],
                "affordable": ["affordable", "budget", "cheap", "economical", "value", "discount"],
                "quality": ["quality", "reliable", "trusted", "professional", "expert", "certified"],
                "innovative": ["innovative", "cutting-edge", "advanced", "modern", "next-gen"],
                "traditional": ["traditional", "classic", "established", "heritage", "authentic"],
                "family": ["family", "friendly", "welcoming", "personal", "caring", "supportive"]
            },
            "min_frequency": 1,
            "enable_stemming": False
        },
        "regional_analyzer": {
            "zip_to_region_mapping": {},
            "state_mappings": {},
            "metro_area_mappings": {},
            "economic_indicators": {},
            "demographic_indicators": {}
        },
        "global_settings": {
            "enable_statistics": True,
            "log_level": "INFO",
            "max_processing_time": 30.0
        }
    }
    
    @classmethod
    def load_from_file(cls, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
            
        Raises:
            ProcessingLayerError: If file cannot be loaded or is invalid
        """
        try:
            path = Path(config_path)
            if not path.exists():
                raise ProcessingLayerError(f"Configuration file not found: {config_path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate configuration
            cls.validate_config(config)
            
            return config
            
        except json.JSONDecodeError as e:
            raise ProcessingLayerError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ProcessingLayerError(f"Failed to load configuration: {e}")
    
    @classmethod
    def save_to_file(cls, config: Dict[str, Any], config_path: str) -> None:
        """
        Save configuration to JSON file.
        
        Args:
            config: Configuration dictionary
            config_path: Path to save configuration file
            
        Raises:
            ProcessingLayerError: If configuration cannot be saved
        """
        try:
            # Validate configuration before saving
            cls.validate_config(config)
            
            path = Path(config_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise ProcessingLayerError(f"Failed to save configuration: {e}")
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def merge_configs(cls, base_config: Dict[str, Any], 
                     override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configurations with override taking precedence.
        
        Args:
            base_config: Base configuration
            override_config: Configuration to override with
            
        Returns:
            Merged configuration dictionary
        """
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = cls.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and values.
        
        Args:
            config: Configuration to validate
            
        Raises:
            ProcessingLayerError: If configuration is invalid
        """
        if not isinstance(config, dict):
            raise ProcessingLayerError("Configuration must be a dictionary")
        
        # Validate required sections
        required_sections = ["tone_analyzer", "keyword_extractor", "regional_analyzer"]
        for section in required_sections:
            if section not in config:
                raise ProcessingLayerError(f"Missing required configuration section: {section}")
            
            if not isinstance(config[section], dict):
                raise ProcessingLayerError(f"Configuration section '{section}' must be a dictionary")
        
        # Validate analyzer configs
        cls._validate_tone_analyzer_config(config["tone_analyzer"])
        cls._validate_keyword_extractor_config(config["keyword_extractor"])
        cls._validate_regional_analyzer_config(config["regional_analyzer"])
        
        # Validate global settings if present
        if "global_settings" in config:
            cls._validate_global_config(config["global_settings"])
    
    @classmethod
    def _validate_tone_analyzer_config(cls, config: Dict[str, Any]) -> None:
        """Validate tone analyzer configuration."""
        list_fields = ["local_indicators", "corporate_indicators", "technical_terms"]
        for field in list_fields:
            if field in config and not isinstance(config[field], list):
                raise ProcessingLayerError(f"Tone analyzer config '{field}' must be a list")
        
        dict_fields = ["sentiment_words", "tone_weights"]
        for field in dict_fields:
            if field in config and not isinstance(config[field], dict):
                raise ProcessingLayerError(f"Tone analyzer config '{field}' must be a dictionary")
    
    @classmethod
    def _validate_keyword_extractor_config(cls, config: Dict[str, Any]) -> None:
        """Validate keyword extractor configuration."""
        dict_fields = ["industry_keywords", "business_type_keywords", "brand_attribute_keywords"]
        for field in dict_fields:
            if field in config and not isinstance(config[field], dict):
                raise ProcessingLayerError(f"Keyword extractor config '{field}' must be a dictionary")
        
        list_fields = ["technology_keywords", "location_keywords"]
        for field in list_fields:
            if field in config and not isinstance(config[field], list):
                raise ProcessingLayerError(f"Keyword extractor config '{field}' must be a list")
        
        if "min_frequency" in config and not isinstance(config["min_frequency"], int):
            raise ProcessingLayerError("Keyword extractor config 'min_frequency' must be an integer")
        
        if "enable_stemming" in config and not isinstance(config["enable_stemming"], bool):
            raise ProcessingLayerError("Keyword extractor config 'enable_stemming' must be a boolean")
    
    @classmethod
    def _validate_regional_analyzer_config(cls, config: Dict[str, Any]) -> None:
        """Validate regional analyzer configuration."""
        dict_fields = ["zip_to_region_mapping", "state_mappings", "metro_area_mappings", 
                      "economic_indicators", "demographic_indicators"]
        for field in dict_fields:
            if field in config and not isinstance(config[field], dict):
                raise ProcessingLayerError(f"Regional analyzer config '{field}' must be a dictionary")
    
    @classmethod
    def _validate_global_config(cls, config: Dict[str, Any]) -> None:
        """Validate global configuration."""
        boolean_fields = ["enable_statistics"]
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                raise ProcessingLayerError(f"Global config '{field}' must be a boolean")
        
        if "max_processing_time" in config:
            if not isinstance(config["max_processing_time"], (int, float)) or config["max_processing_time"] <= 0:
                raise ProcessingLayerError("Global config 'max_processing_time' must be a positive number")
        
        if "log_level" in config:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if config["log_level"] not in valid_levels:
                raise ProcessingLayerError(f"Global config 'log_level' must be one of: {valid_levels}")

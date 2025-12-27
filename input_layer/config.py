"""
Configuration utilities for the Input Layer module.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path

from .exceptions import ConfigurationError


class ConfigManager:
    """Manager for Input Layer configuration."""
    
    DEFAULT_CONFIG = {
        "competitor_handler": {
            "min_length": 2,
            "max_length": 100,
            "allow_numbers": False,
            "allowed_special_chars": " &.-'",
            "normalize_case": True,
            "remove_extra_spaces": True
        },
        "hashtag_handler": {
            "min_length": 1,
            "max_length": 100,
            "allow_numbers": True,
            "allow_underscores": True,
            "normalize_case": True,
            "remove_duplicates": True,
            "max_hashtags": 30,
            "forbidden_words": []
        },
        "zipcode_handler": {
            "supported_formats": ["5", "5+4", "9"],
            "normalize_format": "5+4",
            "country": "US",
            "validate_existence": False,
            "allow_international": False,
            "strict_validation": True
        },
        "global_settings": {
            "enable_statistics": True,
            "log_level": "INFO",
            "max_batch_size": 1000
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
            ConfigurationError: If file cannot be loaded or is invalid
        """
        try:
            path = Path(config_path)
            if not path.exists():
                raise ConfigurationError(f"Configuration file not found: {config_path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate configuration
            cls.validate_config(config)
            
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
    
    @classmethod
    def save_to_file(cls, config: Dict[str, Any], config_path: str) -> None:
        """
        Save configuration to JSON file.
        
        Args:
            config: Configuration dictionary
            config_path: Path to save configuration file
            
        Raises:
            ConfigurationError: If configuration cannot be saved
        """
        try:
            # Validate configuration before saving
            cls.validate_config(config)
            
            path = Path(config_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
    
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
            ConfigurationError: If configuration is invalid
        """
        if not isinstance(config, dict):
            raise ConfigurationError("Configuration must be a dictionary")
        
        # Validate required sections
        required_sections = ["competitor_handler", "hashtag_handler", "zipcode_handler"]
        for section in required_sections:
            if section not in config:
                raise ConfigurationError(f"Missing required configuration section: {section}")
            
            if not isinstance(config[section], dict):
                raise ConfigurationError(f"Configuration section '{section}' must be a dictionary")
        
        # Validate competitor handler config
        cls._validate_competitor_config(config["competitor_handler"])
        
        # Validate hashtag handler config
        cls._validate_hashtag_config(config["hashtag_handler"])
        
        # Validate zipcode handler config
        cls._validate_zipcode_config(config["zipcode_handler"])
        
        # Validate global settings if present
        if "global_settings" in config:
            cls._validate_global_config(config["global_settings"])
    
    @classmethod
    def _validate_competitor_config(cls, config: Dict[str, Any]) -> None:
        """Validate competitor handler configuration."""
        numeric_fields = ["min_length", "max_length"]
        for field in numeric_fields:
            if field in config and not isinstance(config[field], int):
                raise ConfigurationError(f"Competitor config '{field}' must be an integer")
        
        boolean_fields = ["allow_numbers", "normalize_case", "remove_extra_spaces"]
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                raise ConfigurationError(f"Competitor config '{field}' must be a boolean")
        
        if "min_length" in config and "max_length" in config:
            if config["min_length"] > config["max_length"]:
                raise ConfigurationError("Competitor min_length cannot be greater than max_length")
    
    @classmethod
    def _validate_hashtag_config(cls, config: Dict[str, Any]) -> None:
        """Validate hashtag handler configuration."""
        numeric_fields = ["min_length", "max_length", "max_hashtags"]
        for field in numeric_fields:
            if field in config and not isinstance(config[field], int):
                raise ConfigurationError(f"Hashtag config '{field}' must be an integer")
        
        boolean_fields = ["allow_numbers", "allow_underscores", "normalize_case", "remove_duplicates"]
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                raise ConfigurationError(f"Hashtag config '{field}' must be a boolean")
        
        if "forbidden_words" in config and not isinstance(config["forbidden_words"], list):
            raise ConfigurationError("Hashtag config 'forbidden_words' must be a list")
    
    @classmethod
    def _validate_zipcode_config(cls, config: Dict[str, Any]) -> None:
        """Validate zipcode handler configuration."""
        if "supported_formats" in config:
            if not isinstance(config["supported_formats"], list):
                raise ConfigurationError("Zipcode config 'supported_formats' must be a list")
            
            valid_formats = ["5", "5+4", "9"]
            for fmt in config["supported_formats"]:
                if fmt not in valid_formats:
                    raise ConfigurationError(f"Zipcode config 'supported_formats' contains invalid format: {fmt}")
        
        if "normalize_format" in config:
            valid_formats = ["5", "5+4", "9"]
            if config["normalize_format"] not in valid_formats:
                raise ConfigurationError(f"Zipcode config 'normalize_format' must be one of: {valid_formats}")
        
        boolean_fields = ["validate_existence", "allow_international", "strict_validation"]
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                raise ConfigurationError(f"Zipcode config '{field}' must be a boolean")
    
    @classmethod
    def _validate_global_config(cls, config: Dict[str, Any]) -> None:
        """Validate global configuration."""
        boolean_fields = ["enable_statistics"]
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                raise ConfigurationError(f"Global config '{field}' must be a boolean")
        
        if "max_batch_size" in config:
            if not isinstance(config["max_batch_size"], int) or config["max_batch_size"] <= 0:
                raise ConfigurationError("Global config 'max_batch_size' must be a positive integer")
        
        if "log_level" in config:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if config["log_level"] not in valid_levels:
                raise ConfigurationError(f"Global config 'log_level' must be one of: {valid_levels}")

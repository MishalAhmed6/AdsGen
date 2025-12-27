"""
Configuration utilities for the AI Generation Layer module.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

from .exceptions import ConfigurationError


class AIGenerationConfigManager:
    """Manager for AI Generation Layer configuration."""
    
    DEFAULT_CONFIG = {
        "provider": {
            "api_key": None,  # Will be loaded from environment
            "model_name": "gemini-1.5-flash",
            "temperature": 0.7,
            "max_output_tokens": 1024,
            "safety_settings": {
                "harassment": "BLOCK_MEDIUM_AND_ABOVE",
                "hate_speech": "BLOCK_MEDIUM_AND_ABOVE",
                "sexually_explicit": "BLOCK_MEDIUM_AND_ABOVE",
                "dangerous_content": "BLOCK_MEDIUM_AND_ABOVE"
            }
        },
        "templates": {
            "custom_templates": {},
            "tone_weights": {
                "local": 0.4,
                "corporate": 0.3,
                "technical": 0.2,
                "professional": 0.1
            }
        },
        "validation": {
            "min_quality_score": 0.6,
            "enable_content_validation": True,
            "max_retry_attempts": 3,
            "content_length_limits": {
                "headline": 60,
                "ad_text": 200,
                "hashtags": 5,
                "cta": 50
            }
        },
        "global_settings": {
            "enable_statistics": True,
            "log_level": "INFO",
            "cache_responses": False,
            "max_generation_time": 30.0
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
    def load_from_environment(cls, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Args:
            config: Base configuration to merge with environment variables
            
        Returns:
            Configuration dictionary with environment variables loaded
        """
        base_config = config or cls.get_default_config()
        
        # Load API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            base_config["provider"]["api_key"] = api_key
        
        # Load other environment variables
        env_mappings = {
            "AI_GEN_MODEL_NAME": ("provider", "model_name"),
            "AI_GEN_TEMPERATURE": ("provider", "temperature"),
            "AI_GEN_MAX_TOKENS": ("provider", "max_output_tokens"),
            "AI_GEN_LOG_LEVEL": ("global_settings", "log_level"),
            "AI_GEN_CACHE_RESPONSES": ("global_settings", "cache_responses"),
            "AI_GEN_MAX_GENERATION_TIME": ("global_settings", "max_generation_time")
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Navigate to the config path and set the value
                current = base_config
                for key in config_path[:-1]:
                    current = current[key]
                
                # Convert value to appropriate type
                final_key = config_path[-1]
                if final_key in ["temperature", "max_generation_time"]:
                    current[final_key] = float(value)
                elif final_key in ["max_output_tokens"]:
                    current[final_key] = int(value)
                elif final_key in ["cache_responses"]:
                    current[final_key] = value.lower() in ("true", "1", "yes")
                else:
                    current[final_key] = value
        
        return base_config
    
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
        required_sections = ["provider", "templates", "validation", "global_settings"]
        for section in required_sections:
            if section not in config:
                raise ConfigurationError(f"Missing required configuration section: {section}")
            
            if not isinstance(config[section], dict):
                raise ConfigurationError(f"Configuration section '{section}' must be a dictionary")
        
        # Validate provider config
        cls._validate_provider_config(config["provider"])
        
        # Validate templates config
        cls._validate_templates_config(config["templates"])
        
        # Validate validation config
        cls._validate_validation_config(config["validation"])
        
        # Validate global settings
        cls._validate_global_config(config["global_settings"])
    
    @classmethod
    def _validate_provider_config(cls, config: Dict[str, Any]) -> None:
        """Validate provider configuration."""
        if "model_name" in config and not isinstance(config["model_name"], str):
            raise ConfigurationError("Provider config 'model_name' must be a string")
        
        if "temperature" in config:
            if not isinstance(config["temperature"], (int, float)):
                raise ConfigurationError("Provider config 'temperature' must be a number")
            if not 0 <= config["temperature"] <= 2:
                raise ConfigurationError("Provider config 'temperature' must be between 0 and 2")
        
        if "max_output_tokens" in config:
            if not isinstance(config["max_output_tokens"], int):
                raise ConfigurationError("Provider config 'max_output_tokens' must be an integer")
            if config["max_output_tokens"] <= 0:
                raise ConfigurationError("Provider config 'max_output_tokens' must be positive")
    
    @classmethod
    def _validate_templates_config(cls, config: Dict[str, Any]) -> None:
        """Validate templates configuration."""
        if "custom_templates" in config and not isinstance(config["custom_templates"], dict):
            raise ConfigurationError("Templates config 'custom_templates' must be a dictionary")
        
        if "tone_weights" in config:
            if not isinstance(config["tone_weights"], dict):
                raise ConfigurationError("Templates config 'tone_weights' must be a dictionary")
            
            for tone, weight in config["tone_weights"].items():
                if not isinstance(weight, (int, float)):
                    raise ConfigurationError(f"Tone weight for '{tone}' must be a number")
                if not 0 <= weight <= 1:
                    raise ConfigurationError(f"Tone weight for '{tone}' must be between 0 and 1")
    
    @classmethod
    def _validate_validation_config(cls, config: Dict[str, Any]) -> None:
        """Validate validation configuration."""
        if "min_quality_score" in config:
            if not isinstance(config["min_quality_score"], (int, float)):
                raise ConfigurationError("Validation config 'min_quality_score' must be a number")
            if not 0 <= config["min_quality_score"] <= 1:
                raise ConfigurationError("Validation config 'min_quality_score' must be between 0 and 1")
        
        if "enable_content_validation" in config and not isinstance(config["enable_content_validation"], bool):
            raise ConfigurationError("Validation config 'enable_content_validation' must be a boolean")
        
        if "max_retry_attempts" in config:
            if not isinstance(config["max_retry_attempts"], int):
                raise ConfigurationError("Validation config 'max_retry_attempts' must be an integer")
            if config["max_retry_attempts"] < 0:
                raise ConfigurationError("Validation config 'max_retry_attempts' must be non-negative")
        
        if "content_length_limits" in config:
            if not isinstance(config["content_length_limits"], dict):
                raise ConfigurationError("Validation config 'content_length_limits' must be a dictionary")
            
            for content_type, limit in config["content_length_limits"].items():
                if not isinstance(limit, int):
                    raise ConfigurationError(f"Length limit for '{content_type}' must be an integer")
                if limit <= 0:
                    raise ConfigurationError(f"Length limit for '{content_type}' must be positive")
    
    @classmethod
    def _validate_global_config(cls, config: Dict[str, Any]) -> None:
        """Validate global configuration."""
        if "enable_statistics" in config and not isinstance(config["enable_statistics"], bool):
            raise ConfigurationError("Global config 'enable_statistics' must be a boolean")
        
        if "log_level" in config:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if config["log_level"] not in valid_levels:
                raise ConfigurationError(f"Global config 'log_level' must be one of: {valid_levels}")
        
        if "cache_responses" in config and not isinstance(config["cache_responses"], bool):
            raise ConfigurationError("Global config 'cache_responses' must be a boolean")
        
        if "max_generation_time" in config:
            if not isinstance(config["max_generation_time"], (int, float)):
                raise ConfigurationError("Global config 'max_generation_time' must be a number")
            if config["max_generation_time"] <= 0:
                raise ConfigurationError("Global config 'max_generation_time' must be positive")

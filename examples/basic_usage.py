"""
Basic usage examples for the Input Layer module.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_layer import InputLayer, InputData, InputType
from input_layer.config import ConfigManager


def basic_example():
    """Basic usage example."""
    print("=== Basic Input Layer Usage ===")
    
    # Initialize with default configuration
    input_layer = InputLayer()
    
    # Process different types of data
    examples = [
        ("McDonald's Corporation", InputType.COMPETITOR_NAME),
        ("#marketing #digital #strategy #growth", InputType.HASHTAG),
        ("12345-6789", InputType.ZIP_CODE)
    ]
    
    for data, input_type in examples:
        print(f"\nProcessing: {data}")
        result = input_layer.process_single(data, input_type)
        print(f"Processed: {result.processed_data}")
        print(f"Valid: {result.validation_result.is_valid}")
        if result.validation_result.warnings:
            print(f"Warnings: {result.validation_result.warnings}")


def batch_processing_example():
    """Batch processing example."""
    print("\n=== Batch Processing Example ===")
    
    input_layer = InputLayer()
    
    # Batch process competitor names
    competitors = ["apple inc.", "microsoft corp", "google llc", "amazon.com"]
    results = input_layer.process_batch(competitors, InputType.COMPETITOR_NAME)
    
    print("Batch Results:")
    for result in results:
        print(f"  {result.original_data} -> {result.processed_data}")


def custom_configuration_example():
    """Custom configuration example."""
    print("\n=== Custom Configuration Example ===")
    
    # Create custom configuration
    config = {
        "competitor_handler": {
            "min_length": 3,
            "max_length": 50,
            "normalize_case": True
        },
        "hashtag_handler": {
            "max_hashtags": 5,
            "forbidden_words": ["spam", "fake"]
        }
    }
    
    input_layer = InputLayer(config)
    
    # Test with custom config
    result = input_layer.process_single("#spam #marketing", InputType.HASHTAG)
    print(f"Hashtag result: {result.processed_data}")
    print(f"Errors: {result.validation_result.errors}")


if __name__ == "__main__":
    basic_example()
    batch_processing_example()
    custom_configuration_example()

"""
Processing Layer usage examples with Input Layer integration.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_layer import InputLayer, InputType
from processing_layer import ProcessingLayer


def basic_processing_example():
    """Basic Processing Layer usage example."""
    print("=== Basic Processing Layer Usage ===")
    
    # Initialize Input Layer
    input_layer = InputLayer()
    
    # Initialize Processing Layer
    processing_layer = ProcessingLayer()
    
    # Sample data
    sample_data = [
        "Apple Inc.",
        "Microsoft Corporation", 
        "#tech #innovation #software",
        "12345-6789"
    ]
    
    input_types = [
        InputType.COMPETITOR_NAME,
        InputType.COMPETITOR_NAME,
        InputType.HASHTAG,
        InputType.ZIP_CODE
    ]
    
    # Process data through Input Layer
    processed_results = []
    for data, input_type in zip(sample_data, input_types):
        result = input_layer.process_single(data, input_type)
        processed_results.append(result.to_dict())
    
    # Build marketing context using Processing Layer
    context = processing_layer.build_context(processed_results)
    
    print(f"Primary Tone: {context.tone_analysis.primary_tone.value}")
    print(f"Sentiment: {context.tone_analysis.sentiment.value}")
    print(f"Confidence: {context.confidence_score:.2f}")
    print(f"Total Keywords: {len(context.keyword_patterns.get_all_keywords())}")
    print(f"Primary Region: {context.regional_info.primary_region}")


def individual_analysis_example():
    """Example of individual analysis components."""
    print("\n=== Individual Analysis Components ===")
    
    # Sample processed data
    processed_data = [
        {
            "input_type": "competitor_name",
            "processed_data": "Local Family Bakery",
            "validation_result": {"is_valid": True}
        },
        {
            "input_type": "hashtag", 
            "processed_data": "#local #fresh #handmade #community",
            "validation_result": {"is_valid": True}
        },
        {
            "input_type": "zip_code",
            "processed_data": "10001",
            "validation_result": {"is_valid": True}
        }
    ]
    
    processing_layer = ProcessingLayer()
    
    # Individual analyses
    tone_analysis = processing_layer.analyze_tone_only(processed_data)
    print(f"Tone Analysis - Primary: {tone_analysis.primary_tone.value}")
    print(f"Local Indicators: {tone_analysis.local_indicators}")
    
    keyword_patterns = processing_layer.extract_keywords_only(processed_data)
    print(f"Keyword Patterns - Industries: {keyword_patterns.industry_keywords}")
    print(f"Common Patterns: {keyword_patterns.common_patterns}")
    
    regional_info = processing_layer.analyze_regional_only(processed_data)
    print(f"Regional Info - Region: {regional_info.primary_region}")
    print(f"Market Characteristics: {regional_info.market_characteristics}")


def custom_configuration_example():
    """Example with custom configuration."""
    print("\n=== Custom Configuration Example ===")
    
    # Custom configuration
    config = {
        "tone_analyzer": {
            "local_indicators": ["family", "local", "community", "artisan"],
            "corporate_indicators": ["corp", "inc", "llc", "enterprise"]
        },
        "keyword_extractor": {
            "industry_keywords": {
                "food": ["bakery", "restaurant", "cafe", "food"],
                "retail": ["store", "shop", "boutique", "market"]
            }
        }
    }
    
    processing_layer = ProcessingLayer(config)
    
    # Sample data
    processed_data = [
        {
            "input_type": "competitor_name",
            "processed_data": "Family Artisan Bakery",
            "validation_result": {"is_valid": True}
        },
        {
            "input_type": "hashtag",
            "processed_data": "#bakery #fresh #local #family",
            "validation_result": {"is_valid": True}
        }
    ]
    
    context = processing_layer.build_context(processed_data)
    
    print(f"Detected Tone: {context.tone_analysis.primary_tone.value}")
    print(f"Industries Found: {context.keyword_patterns.industry_keywords}")
    print(f"Local Indicators: {context.tone_analysis.local_indicators}")


def export_example():
    """Example of exporting context data."""
    print("\n=== Export Example ===")
    
    processing_layer = ProcessingLayer()
    
    # Sample data
    processed_data = [
        {
            "input_type": "competitor_name",
            "processed_data": "Tech Solutions Inc.",
            "validation_result": {"is_valid": True}
        },
        {
            "input_type": "hashtag",
            "processed_data": "#technology #innovation #software",
            "validation_result": {"is_valid": True}
        },
        {
            "input_type": "zip_code",
            "processed_data": "94102",
            "validation_result": {"is_valid": True}
        }
    ]
    
    context = processing_layer.build_context(processed_data)
    
    # Export as JSON
    json_export = processing_layer.export_context(context, "json")
    print("JSON Export (first 200 chars):")
    print(json_export[:200] + "...")
    
    # Export as summary
    summary_export = processing_layer.export_context(context, "summary")
    print("\nSummary Export:")
    print(summary_export)


if __name__ == "__main__":
    basic_processing_example()
    individual_analysis_example()
    custom_configuration_example()
    export_example()

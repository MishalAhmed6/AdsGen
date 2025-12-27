"""
Complete integrated example showing Input Layer + Processing Layer workflow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_layer import InputLayer, InputType
from processing_layer import ProcessingLayer


def complete_workflow_example():
    """Complete workflow from raw input to marketing context."""
    print("=== Complete Input Layer + Processing Layer Workflow ===")
    
    # Step 1: Initialize both layers
    input_layer = InputLayer()
    processing_layer = ProcessingLayer()
    
    # Step 2: Raw input data
    raw_data = {
        "competitors": [
            "Apple Inc.",
            "Microsoft Corporation",
            "Local Family Bakery",
            "Tech Solutions LLC"
        ],
        "hashtags": [
            "#technology #innovation #software",
            "#local #fresh #handmade #community",
            "#digital #marketing #growth"
        ],
        "zip_codes": [
            "10001",  # New York
            "94102",  # San Francisco
            "90210"   # Beverly Hills
        ]
    }
    
    print("Raw Input Data:")
    for category, items in raw_data.items():
        print(f"  {category}: {items}")
    
    # Step 3: Process through Input Layer
    print("\n=== Input Layer Processing ===")
    processed_results = []
    
    # Process competitors
    for competitor in raw_data["competitors"]:
        result = input_layer.process_single(competitor, InputType.COMPETITOR_NAME)
        processed_results.append(result.to_dict())
        print(f"  {competitor} -> {result.processed_data} (Valid: {result.validation_result.is_valid})")
    
    # Process hashtags
    for hashtags in raw_data["hashtags"]:
        result = input_layer.process_single(hashtags, InputType.HASHTAG)
        processed_results.append(result.to_dict())
        print(f"  {hashtags} -> {result.processed_data} (Valid: {result.validation_result.is_valid})")
    
    # Process ZIP codes
    for zip_code in raw_data["zip_codes"]:
        result = input_layer.process_single(zip_code, InputType.ZIP_CODE)
        processed_results.append(result.to_dict())
        print(f"  {zip_code} -> {result.processed_data} (Valid: {result.validation_result.is_valid})")
    
    # Step 4: Build marketing context using Processing Layer
    print("\n=== Processing Layer Analysis ===")
    context = processing_layer.build_context(processed_results)
    
    # Step 5: Display results
    print("\n=== Marketing Context Results ===")
    
    # Tone Analysis
    print("TONE ANALYSIS:")
    print(f"  Primary Tone: {context.tone_analysis.primary_tone.value}")
    print(f"  Secondary Tones: {[t.value for t in context.tone_analysis.secondary_tones]}")
    print(f"  Sentiment: {context.tone_analysis.sentiment.value}")
    print(f"  Confidence: {context.tone_analysis.confidence:.2f}")
    
    if context.tone_analysis.local_indicators:
        print(f"  Local Indicators: {', '.join(context.tone_analysis.local_indicators)}")
    
    if context.tone_analysis.corporate_indicators:
        print(f"  Corporate Indicators: {', '.join(context.tone_analysis.corporate_indicators)}")
    
    # Keyword Patterns
    print("\nKEYWORD PATTERNS:")
    total_keywords = len(context.keyword_patterns.get_all_keywords())
    print(f"  Total Keywords: {total_keywords}")
    
    if context.keyword_patterns.industry_keywords:
        print(f"  Industries: {', '.join(context.keyword_patterns.industry_keywords)}")
    
    if context.keyword_patterns.technology_keywords:
        print(f"  Technologies: {', '.join(context.keyword_patterns.technology_keywords)}")
    
    if context.keyword_patterns.business_type_keywords:
        print(f"  Business Types: {', '.join(context.keyword_patterns.business_type_keywords)}")
    
    if context.keyword_patterns.common_patterns:
        print(f"  Common Patterns: {', '.join(context.keyword_patterns.common_patterns[:5])}")
    
    # Regional Information
    print("\nREGIONAL INFORMATION:")
    if context.regional_info.primary_region:
        print(f"  Primary Region: {context.regional_info.primary_region}")
    
    if context.regional_info.region_type:
        print(f"  Region Type: {context.regional_info.region_type.value}")
    
    if context.regional_info.state:
        print(f"  State: {context.regional_info.state}")
    
    if context.regional_info.metro_area:
        print(f"  Metro Area: {context.regional_info.metro_area}")
    
    if context.regional_info.population_density:
        print(f"  Population Density: {context.regional_info.population_density}")
    
    if context.regional_info.market_characteristics:
        print(f"  Market Characteristics: {', '.join(context.regional_info.market_characteristics[:5])}")
    
    # Overall Summary
    print(f"\nOVERALL ANALYSIS:")
    print(f"  Confidence Score: {context.confidence_score:.2f}")
    print(f"  Processing Timestamp: {context.processing_timestamp}")
    
    # Step 6: Export for AI generation
    print("\n=== Export for AI Generation ===")
    json_context = processing_layer.export_context(context, "json")
    print(f"JSON Context Length: {len(json_context)} characters")
    
    # Step 7: Statistics
    print("\n=== Processing Statistics ===")
    input_stats = input_layer.get_statistics()
    processing_stats = processing_layer.get_statistics()
    
    print(f"Input Layer - Processed: {input_stats['statistics']['total_processed']}")
    print(f"Processing Layer - Processed: {processing_stats['statistics']['total_processed']}")
    print(f"Processing Layer - Success Rate: {processing_stats['success_rate']:.1f}%")


def batch_processing_example():
    """Example of batch processing multiple datasets."""
    print("\n=== Batch Processing Example ===")
    
    input_layer = InputLayer()
    processing_layer = ProcessingLayer()
    
    # Multiple datasets
    datasets = [
        {
            "name": "Tech Company",
            "data": [
                ("Google LLC", InputType.COMPETITOR_NAME),
                ("#ai #machinelearning #innovation", InputType.HASHTAG),
                ("94043", InputType.ZIP_CODE)  # Mountain View
            ]
        },
        {
            "name": "Local Business",
            "data": [
                ("Corner Coffee Shop", InputType.COMPETITOR_NAME),
                ("#local #coffee #community", InputType.HASHTAG),
                ("60601", InputType.ZIP_CODE)  # Chicago
            ]
        },
        {
            "name": "Healthcare Provider",
            "data": [
                ("Family Medical Clinic", InputType.COMPETITOR_NAME),
                ("#health #medical #wellness", InputType.HASHTAG),
                ("77001", InputType.ZIP_CODE)  # Houston
            ]
        }
    ]
    
    contexts = []
    
    for dataset in datasets:
        print(f"\nProcessing: {dataset['name']}")
        
        # Process through Input Layer
        processed_results = []
        for data, input_type in dataset['data']:
            result = input_layer.process_single(data, input_type)
            processed_results.append(result.to_dict())
        
        # Build context through Processing Layer
        context = processing_layer.build_context(processed_results)
        contexts.append((dataset['name'], context))
        
        # Quick summary
        print(f"  Tone: {context.tone_analysis.primary_tone.value}")
        print(f"  Keywords: {len(context.keyword_patterns.get_all_keywords())}")
        print(f"  Region: {context.regional_info.primary_region}")
    
    # Compare results
    print("\n=== Comparison Summary ===")
    for name, context in contexts:
        print(f"{name}:")
        print(f"  Tone: {context.tone_analysis.primary_tone.value}")
        print(f"  Industries: {', '.join(context.keyword_patterns.industry_keywords)}")
        print(f"  Market Type: {context.regional_info.region_type.value if context.regional_info.region_type else 'Unknown'}")


if __name__ == "__main__":
    complete_workflow_example()
    batch_processing_example()

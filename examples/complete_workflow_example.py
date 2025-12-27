"""
Complete workflow example: Input Layer + Processing Layer + AI Generation Layer
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_layer import InputLayer, InputType
from processing_layer import ProcessingLayer
from ai_generation_layer import AIGenerationLayer


def complete_workflow_example():
    """Complete workflow from raw input to AI-generated marketing content."""
    print("=== Complete Workflow: Input → Processing → AI Generation ===")
    
    # Step 1: Initialize all layers
    print("\n1. Initializing all layers...")
    input_layer = InputLayer()
    processing_layer = ProcessingLayer()
    ai_generator = AIGenerationLayer()
    
    # Step 2: Collect interactive input and process through Input Layer
    print("\n2. Collecting your input and processing...")
    user_results = input_layer.prompt_user_and_process()
    print("\n3. Input Layer Processing:")
    processed_results = []
    
    # Aggregate and print processed outputs
    for r in user_results.get("competitor_names", []):
        processed_results.append(r.to_dict())
        print(f"  {r.original_data} → {r.processed_data}")
    for r in user_results.get("hashtags", []):
        processed_results.append(r.to_dict())
        print(f"  {r.original_data} → {r.processed_data}")
    for r in user_results.get("zip_codes", []):
        processed_results.append(r.to_dict())
        print(f"  {r.original_data} → {r.processed_data}")
    
    # Step 4: Build marketing context using Processing Layer
    print("\n4. Processing Layer Analysis:")
    try:
        marketing_context = processing_layer.build_context(processed_results)
        
        print(f"  Primary Tone: {marketing_context.tone_analysis.primary_tone.value}")
        print(f"  Sentiment: {marketing_context.tone_analysis.sentiment.value}")
        print(f"  Keywords: {len(marketing_context.keyword_patterns.get_all_keywords())}")
        print(f"  Primary Region: {marketing_context.regional_info.primary_region}")
        print(f"  Confidence: {marketing_context.confidence_score:.2f}")
        
    except Exception as e:
        print(f"  Processing Layer failed: {e}")
        return
    
    # Step 5: Collect brand (only) and generate marketing content using AI Generation Layer
    print("\n5. AI Generation Layer:")
    try:
        # Collect only our brand; take competitor + niche hashtag from Input Layer results
        try:
            our_brand = input("Your brand/business name (e.g., Yahoo): ").strip()
        except EOFError:
            our_brand = ""

        # Derive competitor from first processed competitor name (if any)
        derived_competitor = None
        if user_results.get("competitor_names"):
            for r in user_results["competitor_names"]:
                if getattr(r, "processed_data", None):
                    derived_competitor = r.processed_data
                    break

        # Derive niche hashtag from first processed hashtag (if any)
        derived_niche_hashtags = []
        if user_results.get("hashtags"):
            for r in user_results["hashtags"]:
                tag = getattr(r, "processed_data", "")
                if tag:
                    # keep hashtag with '#', also provide a seed without '#'
                    derived_niche_hashtags = [tag]
                    break

        context_dict = marketing_context.to_dict()
        context_dict["business"] = {
            "our_brand": our_brand,
            "competitor": derived_competitor or "",
            "niche_hashtags": derived_niche_hashtags,
        }

        generated_content = ai_generator.generate_content(context_dict)
        
        print("  Generated Marketing Content:")
        print(f"    Headline: {generated_content.headline.content}")
        print(f"    Ad Text: {generated_content.ad_text.content}")
        print(f"    Hashtags: {generated_content.get_hashtags_text()}")
        print(f"    CTA: {generated_content.cta.content}")
        print(f"    Overall Quality: {generated_content.overall_quality.overall_score:.2f}")
        
    except Exception as e:
        print(f"  AI Generation failed: {e}")
        print("  Note: Make sure GEMINI_API_KEY is set in your environment")
        return
    
    # Step 6: Export final content
    print("\n6. Final Content Export:")
    content_dict = generated_content.to_dict()
    print(f"  Content Summary: {generated_content.generate_summary()}")
    
    # Step 7: Show statistics
    print("\n7. Processing Statistics:")
    input_stats = input_layer.get_statistics()
    processing_stats = processing_layer.get_statistics()
    ai_stats = ai_generator.get_statistics()
    
    print(f"  Input Layer: {input_stats['statistics']['total_processed']} processed")
    print(f"  Processing Layer: {processing_stats['success_rate']:.1f}% success rate")
    print(f"  AI Generation: {ai_stats['success_rate']:.1f}% success rate")


def multiple_scenarios_example():
    """Example with multiple different scenarios."""
    print("\n=== Multiple Scenarios Example ===")
    
    scenarios = [
        {
            "name": "Tech Startup",
            "data": [
                ("Innovative Tech Solutions", InputType.COMPETITOR_NAME),
                ("#ai #machinelearning #startup", InputType.HASHTAG),
                ("94043", InputType.ZIP_CODE)  # Mountain View
            ]
        },
        {
            "name": "Local Restaurant",
            "data": [
                ("Family Pizzeria", InputType.COMPETITOR_NAME),
                ("#local #fresh #family #pizza", InputType.HASHTAG),
                ("60601", InputType.ZIP_CODE)  # Chicago
            ]
        },
        {
            "name": "Healthcare Provider",
            "data": [
                ("Metro Medical Center", InputType.COMPETITOR_NAME),
                ("#healthcare #medical #wellness", InputType.HASHTAG),
                ("10001", InputType.ZIP_CODE)  # New York
            ]
        }
    ]
    
    # Initialize layers
    input_layer = InputLayer()
    processing_layer = ProcessingLayer()
    ai_generator = AIGenerationLayer()
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        try:
            # Process through Input Layer
            processed_results = []
            for data, input_type in scenario['data']:
                result = input_layer.process_single(data, input_type)
                processed_results.append(result.to_dict())
            
            # Build context through Processing Layer
            marketing_context = processing_layer.build_context(processed_results)
            
            # Generate content through AI Generation Layer
            generated_content = ai_generator.generate_content(marketing_context.to_dict())
            
            # Show results
            print(f"Tone: {marketing_context.tone_analysis.primary_tone.value}")
            print(f"Region: {marketing_context.regional_info.primary_region}")
            print(f"Headline: {generated_content.headline.content}")
            print(f"CTA: {generated_content.cta.content}")
            print(f"Quality: {generated_content.overall_quality.overall_score:.2f}")
            
        except Exception as e:
            print(f"Failed: {e}")


def quality_analysis_example():
    """Example focusing on content quality analysis."""
    print("\n=== Quality Analysis Example ===")
    
    marketing_context = {
        "tone_analysis": {
            "primary_tone": "corporate",
            "secondary_tones": ["professional", "formal"],
            "sentiment": "positive",
            "confidence": 0.9
        },
        "keyword_patterns": {
            "industry_keywords": ["finance", "technology"],
            "technology_keywords": ["digital", "secure", "automation"],
            "business_type_keywords": ["corporation"],
            "common_patterns": ["financial", "digital"]
        },
        "regional_info": {
            "primary_region": "New York Metro",
            "region_type": "urban",
            "market_characteristics": ["competitive_market", "high_disposable_income", "fast_paced"]
        },
        "confidence_score": 0.88
    }
    
    ai_generator = AIGenerationLayer()
    
    try:
        generated_content = ai_generator.generate_content(marketing_context)
        
        print("Content Quality Analysis:")
        quality = generated_content.overall_quality
        
        print(f"Overall Quality Score: {quality.overall_score:.2f}")
        print(f"Readability Score: {quality.readability_score:.2f}")
        print(f"Engagement Score: {quality.engagement_score:.2f}")
        print(f"Brand Alignment Score: {quality.brand_alignment_score:.2f}")
        print(f"Tone Consistency Score: {quality.tone_consistency_score:.2f}")
        print(f"Length Appropriateness: {quality.length_appropriateness:.2f}")
        
        if quality.quality_issues:
            print(f"\nQuality Issues:")
            for issue in quality.quality_issues:
                print(f"  - {issue}")
        
        if quality.suggestions:
            print(f"\nImprovement Suggestions:")
            for suggestion in quality.suggestions:
                print(f"  - {suggestion}")
        
        print(f"\nGenerated Content:")
        print(f"  Headline: {generated_content.headline.content}")
        print(f"  Ad Text: {generated_content.ad_text.content}")
        print(f"  Hashtags: {generated_content.get_hashtags_text()}")
        print(f"  CTA: {generated_content.cta.content}")
        
    except Exception as e:
        print(f"Quality analysis failed: {e}")


if __name__ == "__main__":
    complete_workflow_example()
    multiple_scenarios_example()
    quality_analysis_example()

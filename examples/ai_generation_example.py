"""
AI Generation Layer usage examples.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_generation_layer import AIGenerationLayer
from ai_generation_layer.config import AIGenerationConfigManager


def basic_ai_generation_example():
    """Basic AI Generation Layer usage example."""
    print("=== Basic AI Generation Layer Usage ===")
    
    # Sample marketing context (from Processing Layer)
    marketing_context = {
        "tone_analysis": {
            "primary_tone": "professional",
            "secondary_tones": ["corporate"],
            "sentiment": "positive",
            "confidence": 0.8,
            "local_indicators": [],
            "corporate_indicators": ["corp", "solutions"],
            "technical_terms": ["software", "technology"]
        },
        "keyword_patterns": {
            "industry_keywords": ["technology"],
            "technology_keywords": ["software", "digital", "innovation"],
            "business_type_keywords": ["corporation"],
            "location_keywords": [],
            "brand_attribute_keywords": ["professional"],
            "common_patterns": ["tech", "software"],
            "frequency_map": {"tech": 2, "software": 3, "innovation": 1}
        },
        "regional_info": {
            "primary_region": "San Francisco Bay Area",
            "region_type": "urban",
            "state": "CA",
            "metro_area": "San Francisco-Oakland-Berkeley",
            "population_density": "High",
            "market_characteristics": ["tech_savvy", "innovation_focused", "high_disposable_income"]
        },
        "confidence_score": 0.85,
        "processing_timestamp": "2024-01-01T12:00:00"
    }
    
    # Initialize AI Generation Layer
    ai_generator = AIGenerationLayer()
    
    # Generate content
    try:
        generated_content = ai_generator.generate_content(marketing_context)
        
        print(f"Headline: {generated_content.headline.content}")
        print(f"Ad Text: {generated_content.ad_text.content}")
        print(f"Hashtags: {generated_content.get_hashtags_text()}")
        print(f"CTA: {generated_content.cta.content}")
        print(f"Overall Quality Score: {generated_content.overall_quality.overall_score:.2f}")
        
    except Exception as e:
        print(f"Generation failed: {e}")
        print("Note: Make sure GEMINI_API_KEY is set in your environment")


def individual_content_generation_example():
    """Example of generating individual content pieces."""
    print("\n=== Individual Content Generation ===")
    
    marketing_context = {
        "tone_analysis": {
            "primary_tone": "local",
            "secondary_tones": ["casual"],
            "sentiment": "positive",
            "confidence": 0.9,
            "local_indicators": ["local", "family", "community"],
            "corporate_indicators": [],
            "technical_terms": []
        },
        "keyword_patterns": {
            "industry_keywords": ["food"],
            "technology_keywords": [],
            "business_type_keywords": [],
            "location_keywords": ["local"],
            "brand_attribute_keywords": ["family"],
            "common_patterns": ["local", "fresh"],
            "frequency_map": {"local": 3, "fresh": 2}
        },
        "regional_info": {
            "primary_region": "Chicago Metro",
            "region_type": "urban",
            "state": "IL",
            "metro_area": "Chicago-Naperville-Elgin",
            "population_density": "High",
            "market_characteristics": ["family_oriented", "competitive_market"]
        }
    }
    
    ai_generator = AIGenerationLayer()
    
    try:
        # Generate individual pieces
        headline = ai_generator.generate_headline_only(marketing_context)
        print(f"Generated Headline: {headline.content}")
        print(f"Headline Quality: {headline.quality_score:.2f}")
        
        ad_text = ai_generator.generate_ad_text_only(marketing_context)
        print(f"Generated Ad Text: {ad_text.content}")
        print(f"Ad Text Quality: {ad_text.quality_score:.2f}")
        
        hashtags = ai_generator.generate_hashtags_only(marketing_context)
        hashtag_texts = [h.content for h in hashtags]
        print(f"Generated Hashtags: {' '.join(hashtag_texts)}")
        
        cta = ai_generator.generate_cta_only(marketing_context)
        print(f"Generated CTA: {cta.content}")
        print(f"CTA Quality: {cta.quality_score:.2f}")
        
    except Exception as e:
        print(f"Generation failed: {e}")


def custom_configuration_example():
    """Example with custom configuration."""
    print("\n=== Custom Configuration Example ===")
    
    # Custom configuration
    config = {
        "provider": {
            "temperature": 0.9,  # More creative
            "max_output_tokens": 512
        },
        "templates": {
            "tone_weights": {
                "local": 0.6,
                "corporate": 0.2,
                "technical": 0.2
            }
        }
    }
    
    marketing_context = {
        "tone_analysis": {
            "primary_tone": "technical",
            "secondary_tones": ["professional"],
            "sentiment": "neutral",
            "confidence": 0.7
        },
        "keyword_patterns": {
            "industry_keywords": ["technology"],
            "technology_keywords": ["ai", "machine learning", "automation"]
        },
        "regional_info": {
            "primary_region": "Silicon Valley",
            "region_type": "urban"
        }
    }
    
    ai_generator = AIGenerationLayer(config)
    
    try:
        generated_content = ai_generator.generate_content(marketing_context)
        
        print(f"Headline: {generated_content.headline.content}")
        print(f"Ad Text: {generated_content.ad_text.content}")
        print(f"Quality Score: {generated_content.overall_quality.overall_score:.2f}")
        
    except Exception as e:
        print(f"Generation failed: {e}")


def export_example():
    """Example of exporting generated content."""
    print("\n=== Export Example ===")
    
    marketing_context = {
        "tone_analysis": {
            "primary_tone": "corporate",
            "sentiment": "positive",
            "confidence": 0.8
        },
        "keyword_patterns": {
            "industry_keywords": ["finance"],
            "technology_keywords": ["digital", "secure"]
        },
        "regional_info": {
            "primary_region": "New York Metro",
            "region_type": "urban"
        }
    }
    
    ai_generator = AIGenerationLayer()
    
    try:
        generated_content = ai_generator.generate_content(marketing_context)
        
        # Export as dictionary
        content_dict = generated_content.to_dict()
        print("Content Dictionary Keys:", list(content_dict.keys()))
        
        # Show summary
        print(f"Summary: {generated_content.generate_summary()}")
        
        # Show quality details
        quality = generated_content.overall_quality
        print(f"Quality Breakdown:")
        print(f"  Readability: {quality.readability_score:.2f}")
        print(f"  Engagement: {quality.engagement_score:.2f}")
        print(f"  Brand Alignment: {quality.brand_alignment_score:.2f}")
        
        if quality.quality_issues:
            print(f"  Issues: {', '.join(quality.quality_issues)}")
        
        if quality.suggestions:
            print(f"  Suggestions: {', '.join(quality.suggestions)}")
        
    except Exception as e:
        print(f"Generation failed: {e}")


def statistics_example():
    """Example of viewing generation statistics."""
    print("\n=== Statistics Example ===")
    
    ai_generator = AIGenerationLayer()
    
    # Show initial stats
    stats = ai_generator.get_statistics()
    print("Initial Statistics:")
    print(f"  Total Generated: {stats['statistics']['total_generated']}")
    print(f"  Success Rate: {stats['success_rate']:.1f}%")
    print(f"  Provider Info: {stats['provider_info']['model_name']}")
    
    # Generate some content to see stats change
    marketing_context = {
        "tone_analysis": {"primary_tone": "professional", "sentiment": "neutral"},
        "keyword_patterns": {"industry_keywords": ["technology"]},
        "regional_info": {"primary_region": "General"}
    }
    
    try:
        generated_content = ai_generator.generate_content(marketing_context)
        
        # Show updated stats
        stats = ai_generator.get_statistics()
        print("\nUpdated Statistics:")
        print(f"  Total Generated: {stats['statistics']['total_generated']}")
        print(f"  Success Rate: {stats['success_rate']:.1f}%")
        
        # Show content type breakdown
        content_types = stats['statistics']['content_types']
        print("  Content Type Breakdown:")
        for content_type, counts in content_types.items():
            print(f"    {content_type}: {counts['successful']}/{counts['generated']} successful")
        
    except Exception as e:
        print(f"Generation failed: {e}")


if __name__ == "__main__":
    basic_ai_generation_example()
    individual_content_generation_example()
    custom_configuration_example()
    export_example()
    statistics_example()

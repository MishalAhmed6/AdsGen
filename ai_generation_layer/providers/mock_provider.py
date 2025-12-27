"""
Mock LLM provider for testing and demonstration purposes.
Generates realistic marketing content without requiring API keys.
"""

import random
import json
from typing import Dict, Any, Optional, List

from ..models.base import BaseLLMProvider
from ..exceptions import ProviderError


class MockProvider(BaseLLMProvider):
    """Mock LLM provider that generates realistic marketing content."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Mock provider with configuration.
        
        Args:
            config: Configuration dictionary (not used in mock)
        """
        super().__init__(config)
        
        # Mock configuration
        self.model_name = "mock-ai-generator"
        self.temperature = 0.7
        self.max_output_tokens = 1024
        
        # Content templates for different contexts
        self._init_content_templates()
    
    def _init_content_templates(self):
        """Initialize content templates for different marketing contexts."""
        
        self.headline_templates = [
            "🚀 Transform Your {industry} with {tech_keyword}",
            "💡 {tech_keyword} Solutions That Drive {business_type} Growth",
            "⚡ Revolutionary {tech_keyword} for Modern {business_type}",
            "🎯 Smart {tech_keyword} for {region_type} {business_type}",
            "🌟 Next-Gen {tech_keyword} Innovation for {industry}",
            "🔧 Advanced {tech_keyword} Solutions - Built for {region_type}",
            "💼 Professional {tech_keyword} Services for {business_type}",
            "🚀 Cutting-Edge {tech_keyword} Technology"
        ]
        
        self.ad_text_templates = [
            "Discover how our {tech_keyword} solutions can revolutionize your {business_type}. With {regional_characteristic} and {market_focus}, we deliver results that matter. Join {success_metric} of satisfied clients who trust our expertise.",
            
            "Experience the power of {tech_keyword} innovation designed for {region_type} {business_type}. Our {tech_keyword} platform combines {tech_feature} with {business_benefit} to drive exceptional outcomes.",
            
            "Unlock your {business_type}'s potential with our advanced {tech_keyword} technology. Built for {regional_characteristic}, our solutions deliver {business_benefit} and measurable results.",
            
            "Transform your {business_type} operations with cutting-edge {tech_keyword}. Our {region_type}-focused approach ensures {business_benefit} while maintaining {quality_standard}.",
            
            "Join the {industry} revolution with our {tech_keyword} solutions. Designed for {regional_characteristic}, we help {business_type} achieve {success_metric} through innovative technology."
        ]
        
        self.hashtag_templates = [
            ["{tech_keyword}", "{industry}", "{business_type}", "{tech_trend}", "{region_short}"],
            ["{tech_keyword}", "Innovation", "{business_type}", "Technology", "Growth"],
            ["{tech_keyword}", "{industry}", "Digital", "{tech_trend}", "Success"],
            ["{tech_keyword}", "{business_type}", "Tech", "Solutions", "Future"],
            ["{tech_keyword}", "{industry}", "Professional", "Services", "Excellence"]
        ]
        
        self.cta_templates = [
            "Start Your {tech_keyword} Journey Today",
            "Get Free {tech_keyword} Consultation",
            "Transform Your {business_type} Now",
            "Discover {tech_keyword} Solutions",
            "Unlock {business_type} Potential",
            "Experience {tech_keyword} Innovation",
            "Join the {industry} Revolution",
            "Schedule Your {tech_keyword} Demo"
        ]
        
        # Dynamic content based on context
        self.tech_keywords = ["AI", "Cloud", "Digital", "Automation", "Analytics", "IoT", "Blockchain", "Machine Learning"]
        self.industries = ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Education", "Real Estate"]
        self.business_types = ["Corporations", "Startups", "SMBs", "Enterprises", "Organizations", "Companies", "Businesses"]
        self.tech_trends = ["AI", "Cloud", "IoT", "Automation", "Digital Transformation", "Smart Solutions"]
        self.regional_characteristics = ["tech-savvy professionals", "innovative businesses", "growth-focused organizations", "forward-thinking companies"]
        self.market_focuses = ["high-performance", "scalable", "enterprise-grade", "innovative", "cutting-edge"]
        self.business_benefits = ["increased efficiency", "reduced costs", "enhanced productivity", "better insights", "competitive advantage"]
        self.success_metrics = ["thousands", "hundreds", "dozens", "numerous", "countless"]
        self.quality_standards = ["industry-leading standards", "premium quality", "exceptional performance", "unmatched reliability"]
        self.tech_features = ["advanced algorithms", "intelligent automation", "real-time analytics", "seamless integration", "robust security"]
    
    def _extract_context_values(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Extract values from marketing context for content generation."""
        values = {}
        
        # Extract tone information
        tone_analysis = context.get("tone_analysis", {})
        primary_tone = tone_analysis.get("primary_tone", "professional")
        values["tone"] = primary_tone
        
        # Extract keyword information
        keyword_patterns = context.get("keyword_patterns", {})
        industry_keywords = keyword_patterns.get("industry_keywords", ["Technology"])
        tech_keywords = keyword_patterns.get("technology_keywords", ["Digital"])
        
        values["industry"] = industry_keywords[0] if industry_keywords else random.choice(self.industries)
        values["tech_keyword"] = tech_keywords[0] if tech_keywords else random.choice(self.tech_keywords)
        values["tech_trend"] = random.choice(self.tech_trends)
        
        # Extract regional information
        regional_info = context.get("regional_info", {})
        region_type = regional_info.get("region_type", "urban")
        metro_area = regional_info.get("metro_area", "Tech Hub")
        
        values["region_type"] = region_type
        values["region_short"] = metro_area.split("-")[0] if "-" in metro_area else metro_area.split(",")[0]
        values["regional_characteristic"] = random.choice(self.regional_characteristics)
        
        # Determine business type based on context
        business_keywords = keyword_patterns.get("business_type_keywords", ["Corporations"])
        values["business_type"] = business_keywords[0] if business_keywords else random.choice(self.business_types)
        
        # Add dynamic content
        values["market_focus"] = random.choice(self.market_focuses)
        values["business_benefit"] = random.choice(self.business_benefits)
        values["success_metric"] = random.choice(self.success_metrics)
        values["quality_standard"] = random.choice(self.quality_standards)
        values["tech_feature"] = random.choice(self.tech_features)
        
        return values
    
    def _generate_headline(self, context_values: Dict[str, str]) -> str:
        """Generate a compelling headline based on context."""
        template = random.choice(self.headline_templates)
        return template.format(**context_values)
    
    def _generate_ad_text(self, context_values: Dict[str, str]) -> str:
        """Generate engaging ad text based on context."""
        template = random.choice(self.ad_text_templates)
        return template.format(**context_values)
    
    def _generate_hashtags(self, context_values: Dict[str, str]) -> List[str]:
        """Generate relevant hashtags based on context."""
        template = random.choice(self.hashtag_templates)
        hashtags = []
        
        for tag_template in template:
            tag = tag_template.format(**context_values)
            # Clean and format hashtag
            tag = tag.replace(" ", "").replace("-", "").title()
            if not tag.startswith("#"):
                tag = f"#{tag}"
            hashtags.append(tag)
        
        return hashtags[:5]  # Limit to 5 hashtags
    
    def _generate_cta(self, context_values: Dict[str, str]) -> str:
        """Generate a compelling call-to-action based on context."""
        template = random.choice(self.cta_templates)
        return template.format(**context_values)
    
    def generate_content(self, prompt: str, **kwargs) -> str:
        """
        Generate content using mock AI.
        
        Args:
            prompt: The prompt containing marketing context
            **kwargs: Additional parameters
            
        Returns:
            Generated content as string
        """
        try:
            # Try to extract context from prompt
            context = {}
            if "{" in prompt and "}" in prompt:
                try:
                    # Extract JSON-like content from prompt
                    start = prompt.find("{")
                    end = prompt.rfind("}") + 1
                    if start >= 0 and end > start:
                        context_str = prompt[start:end]
                        context = json.loads(context_str)
                except:
                    pass
            
            # Extract context values
            context_values = self._extract_context_values(context)
            
            # Generate content based on prompt type
            if "headline" in prompt.lower():
                return self._generate_headline(context_values)
            elif "ad text" in prompt.lower() or "advertisement" in prompt.lower():
                return self._generate_ad_text(context_values)
            elif "hashtag" in prompt.lower():
                hashtags = self._generate_hashtags(context_values)
                return " ".join(hashtags)
            elif "cta" in prompt.lower() or "call to action" in prompt.lower():
                return self._generate_cta(context_values)
            else:
                return self._generate_ad_text(context_values)
                
        except Exception as e:
            raise ProviderError(f"Mock generation failed: {str(e)}") from e
    
    def generate_structured_content(self, prompt: str, expected_format: str = "json", **kwargs) -> Dict[str, Any]:
        """
        Generate structured content using mock AI.
        
        Args:
            prompt: The prompt containing marketing context
            expected_format: Expected format ("json", "list", "dict")
            **kwargs: Additional parameters
            
        Returns:
            Parsed structured content
        """
        try:
            # Try to extract context from prompt
            context = {}
            if "{" in prompt and "}" in prompt:
                try:
                    # Extract JSON-like content from prompt
                    start = prompt.find("{")
                    end = prompt.rfind("}") + 1
                    if start >= 0 and end > start:
                        context_str = prompt[start:end]
                        context = json.loads(context_str)
                except:
                    pass
            
            # Extract context values
            context_values = self._extract_context_values(context)
            
            # Generate structured content
            if expected_format == "json":
                return {
                    "headline": self._generate_headline(context_values),
                    "ad_text": self._generate_ad_text(context_values),
                    "hashtags": self._generate_hashtags(context_values),
                    "cta": self._generate_cta(context_values)
                }
            elif expected_format == "list":
                return [
                    self._generate_headline(context_values),
                    self._generate_ad_text(context_values),
                    *self._generate_hashtags(context_values),
                    self._generate_cta(context_values)
                ]
            else:
                return {
                    "content": self._generate_ad_text(context_values),
                    "metadata": context_values
                }
                
        except Exception as e:
            raise ProviderError(f"Mock structured content generation failed: {str(e)}") from e
    
    def is_available(self) -> bool:
        """
        Check if Mock provider is available (always True).
        
        Returns:
            Always True for mock provider
        """
        return True
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the mock model configuration.
        
        Returns:
            Dictionary with model information
        """
        return {
            "provider": "mock",
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "api_key_configured": True,  # Mock doesn't need API key
            "available": True
        }

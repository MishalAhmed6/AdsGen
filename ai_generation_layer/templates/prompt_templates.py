"""
Prompt templates for AI content generation.
"""

from typing import Dict, Any, List
from ..exceptions import PromptError


class PromptTemplates:
    """Collection of prompt templates for different content types."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize prompt templates with configuration.
        
        Args:
            config: Configuration dictionary with custom templates
        """
        self.config = config or {}
    
    def generate_headline_prompt(self, context: Dict[str, Any]) -> str:
        """
        Generate prompt for headline creation.
        
        Args:
            context: Marketing context from Processing Layer
            
        Returns:
            Formatted prompt for headline generation
        """
        tone_info = context.get("tone_analysis", {})
        keywords = context.get("keyword_patterns", {})
        regional_info = context.get("regional_info", {})
        
        # Extract key information
        primary_tone = tone_info.get("primary_tone", "professional")
        sentiment = tone_info.get("sentiment", "neutral")
        industries = keywords.get("industry_keywords", [])
        technologies = keywords.get("technology_keywords", [])
        region = regional_info.get("primary_region", "")

        # Business details (our brand vs competitor vs niche)
        business = context.get("business", {})
        our_brand = business.get("our_brand", "")
        competitor = business.get("competitor", "")
        niche_hashtags = business.get("niche_hashtags", [])
        offer_type = business.get("offer_type", "")
        
        # Build tone-specific instructions
        tone_instructions = self._get_tone_instructions(primary_tone, sentiment)
        
        # Build industry context
        industry_context = self._build_industry_context(industries, technologies)
        
        # Build regional context
        regional_context = self._build_regional_context(regional_info)
        
        # Avoid defaulting to Technology/Digital; if unknown, leave blank to reduce bias
        industry_text = ', '.join(industries[:2]) if industries else ''
        tech_text = ', '.join(technologies[:2]) if technologies else ''
        
        # Build offer type context
        offer_context = ""
        if offer_type:
            offer_context = self._build_offer_context(offer_type)
        
        # Add competitor intelligence if available
        competitor_desc = business.get("competitor_description", "")
        competitor_services = business.get("competitor_services", [])
        competitor_features = business.get("competitor_features", [])
        intel_source = business.get("intelligence_source", "none")
        
        competitor_context = ""
        if competitor_desc and intel_source != "none":
            competitor_context = f"\nCompetitor Information (from {intel_source}):\n"
            competitor_context += f"Description: {competitor_desc[:300]}\n"
            if competitor_services:
                competitor_context += f"Services: {', '.join(competitor_services[:5])}\n"
            if competitor_features:
                competitor_context += f"Key Features: {', '.join(competitor_features[:5])}\n"
        
        prompt = f"""Create a catchy marketing headline (under 60 characters) for a {primary_tone} tone.

Industry: {industry_text}
Tech focus: {tech_text}
Region: {region}

Our Brand: {our_brand}
Competitor: {competitor}
Niche Hashtags: {' '.join(niche_hashtags) if niche_hashtags else ''}{offer_context}{competitor_context}

Create a competitive headline that highlights how {our_brand} is better than {competitor}. If industry/tech is blank, infer from context without assuming technology. Generate only the headline, no explanations."""

        return prompt
    
    def generate_ad_text_prompt(self, context: Dict[str, Any]) -> str:
        """
        Generate prompt for main ad text creation.
        
        Args:
            context: Marketing context from Processing Layer
            
        Returns:
            Formatted prompt for ad text generation
        """
        tone_info = context.get("tone_analysis", {})
        keywords = context.get("keyword_patterns", {})
        regional_info = context.get("regional_info", {})
        
        # Extract key information
        primary_tone = tone_info.get("primary_tone", "professional")
        secondary_tones = tone_info.get("secondary_tones", [])
        industries = keywords.get("industry_keywords", [])
        technologies = keywords.get("technology_keywords", [])
        business_types = keywords.get("business_type_keywords", [])

        # Business details (our brand vs competitor vs niche)
        business = context.get("business", {})
        our_brand = business.get("our_brand", "")
        competitor = business.get("competitor", "")
        niche_hashtags = business.get("niche_hashtags", [])
        offer_type = business.get("offer_type", "")
        audience_type = business.get("audience_type", "")
        goal = business.get("goal", "")
        
        # Build tone context
        tone_context = self._build_tone_context(primary_tone, secondary_tones)
        
        # Build market context
        market_context = self._build_market_context(industries, technologies, business_types)
        
        # Build regional context
        regional_context = self._build_regional_context(regional_info)
        
        industry_text = ', '.join(industries[:2]) if industries else ''
        tech_text = ', '.join(technologies[:2]) if technologies else ''
        target_text = ', '.join(business_types[:2]) if business_types else ''
        
        # Build offer type context
        offer_context = ""
        if offer_type:
            offer_context = self._build_offer_context(offer_type)
        
        # Add competitor intelligence if available
        competitor_desc = business.get("competitor_description", "")
        competitor_services = business.get("competitor_services", [])
        competitor_features = business.get("competitor_features", [])
        intel_source = business.get("intelligence_source", "none")
        
        competitor_context = ""
        if competitor_desc and intel_source != "none":
            competitor_context = f"\n\nCompetitor Intelligence (from {intel_source}):\n"
            competitor_context += f"About {competitor}: {competitor_desc[:400]}\n"
            if competitor_services:
                competitor_context += f"Their Services: {', '.join(competitor_services[:5])}\n"
            if competitor_features:
                competitor_context += f"Their Key Features: {', '.join(competitor_features[:5])}\n"
            competitor_context += f"\nCreate competitive ad text that highlights how {our_brand} is superior to {competitor} based on this intelligence. Focus on advantages and differentiation."
        
        prompt = f"""Create compelling ad text (2-3 sentences) for a {primary_tone} tone.

Industry: {industry_text}
Tech focus: {tech_text}
Target: {target_text}

Our Brand: {our_brand}
Competitor: {competitor}
Niche Hashtags: {' '.join(niche_hashtags) if niche_hashtags else ''}{offer_context}{competitor_context}

If fields are blank, infer from context (e.g., Education, Healthcare) without defaulting to tech. Focus on benefits and value. Generate only the ad text."""

        return prompt
    
    def generate_hashtags_prompt(self, context: Dict[str, Any]) -> str:
        """
        Generate prompt for hashtag creation.
        
        Args:
            context: Marketing context from Processing Layer
            
        Returns:
            Formatted prompt for hashtag generation
        """
        tone_info = context.get("tone_analysis", {})
        keywords = context.get("keyword_patterns", {})
        regional_info = context.get("regional_info", {})
        business = context.get("business", {})
        our_brand = business.get("our_brand", "")
        competitor = business.get("competitor", "")
        niche_hashtags = business.get("niche_hashtags", [])
        
        # Extract key information
        primary_tone = tone_info.get("primary_tone", "professional")
        industries = keywords.get("industry_keywords", [])
        technologies = keywords.get("technology_keywords", [])
        trends = keywords.get("trend_keywords", [])
        
        # Build relevant keywords context
        relevant_keywords = industries + technologies + trends
        keywords_text = ", ".join(relevant_keywords) if relevant_keywords else "general business"
        
        # Build tone-specific hashtag instructions
        hashtag_style = self._get_hashtag_style(primary_tone)
        
        # Add domain-specific guidance: if Education detected, avoid marketing phrasing
        is_education = any(k.lower() == "education" for k in industries)
        domain_note = (
            "Focus on STEM education; avoid marketing/business/sales terms. "
            if is_education else
            "Avoid generic marketing/business/sales terms unless clearly relevant. "
        )

        prompt = f"""Create 3-5 relevant hashtags for this topic.

Keywords: {keywords_text}
Tone: {primary_tone}
Guidance: {domain_note}Do not assume technology if keywords don't indicate it.

Our Brand: {our_brand}
Competitor: {competitor}
Niche Hashtags (seed): {' '.join(niche_hashtags) if niche_hashtags else ''}

Return only hashtags separated by spaces (e.g., #hashtag1 #hashtag2 #hashtag3)."""

        return prompt
    
    def generate_cta_prompt(self, context: Dict[str, Any]) -> str:
        """
        Generate prompt for call-to-action creation.
        
        Args:
            context: Marketing context from Processing Layer
            
        Returns:
            Formatted prompt for CTA generation
        """
        tone_info = context.get("tone_analysis", {})
        keywords = context.get("keyword_patterns", {})
        regional_info = context.get("regional_info", {})
        
        # Extract key information
        primary_tone = tone_info.get("primary_tone", "professional")
        industries = keywords.get("industry_keywords", [])
        market_characteristics = regional_info.get("market_characteristics", [])
        business = context.get("business", {})
        our_brand = business.get("our_brand", "")
        competitor = business.get("competitor", "")
        offer_type = business.get("offer_type", "")
        
        # Build action context
        action_context = self._build_action_context(industries, market_characteristics)
        
        # Build tone-specific CTA instructions
        cta_style = self._get_cta_style(primary_tone)
        
        # Build offer type context
        offer_context = ""
        if offer_type:
            offer_context = self._build_offer_context(offer_type)
        
        industry_text = ', '.join(industries[:2]) if industries else ''
        prompt = f"""Create a compelling call-to-action (under 50 characters) for {primary_tone} tone.

Industry: {industry_text}

Our Brand: {our_brand}
Competitor: {competitor}{offer_context}

If industry is blank, infer from context without assuming technology. Generate only the CTA text."""

        return prompt
    
    def _get_tone_instructions(self, primary_tone: str, sentiment: str) -> str:
        """Get tone-specific instructions for content generation."""
        tone_instructions = {
            "local": "Write in a friendly, community-focused tone that emphasizes local presence, personal service, and neighborhood connection.",
            "corporate": "Write in a professional, authoritative tone that emphasizes expertise, reliability, and business credibility.",
            "technical": "Write in a precise, innovation-focused tone that emphasizes technical expertise and cutting-edge solutions.",
            "professional": "Write in a balanced, trustworthy tone that emphasizes competence and reliability.",
            "casual": "Write in a relaxed, approachable tone that feels conversational and easy-going.",
            "formal": "Write in a polished, sophisticated tone that emphasizes quality and prestige."
        }
        
        base_instruction = tone_instructions.get(primary_tone, tone_instructions["professional"])
        
        # Add sentiment context
        if sentiment == "positive":
            base_instruction += " Use positive, enthusiastic language that conveys excitement and optimism."
        elif sentiment == "negative":
            base_instruction += " Address concerns directly and focus on solutions and improvements."
        
        return base_instruction
    
    def _build_industry_context(self, industries: List[str], technologies: List[str]) -> str:
        """Build industry-specific context for prompts."""
        context_parts = []
        
        if industries:
            context_parts.append(f"Target Industries: {', '.join(industries)}")
        
        if technologies:
            context_parts.append(f"Technologies: {', '.join(technologies)}")
        
        if not context_parts:
            context_parts.append("General business market")
        
        return "\n".join(context_parts)
    
    def _build_regional_context(self, regional_info: Dict[str, Any]) -> str:
        """Build regional context for prompts."""
        context_parts = []
        
        if regional_info.get("primary_region"):
            context_parts.append(f"Target Region: {regional_info['primary_region']}")
        
        if regional_info.get("region_type"):
            context_parts.append(f"Region Type: {regional_info['region_type']}")
        
        if regional_info.get("market_characteristics"):
            characteristics = regional_info["market_characteristics"][:3]  # Top 3
            context_parts.append(f"Market Characteristics: {', '.join(characteristics)}")
        
        if not context_parts:
            context_parts.append("General geographic market")
        
        return "\n".join(context_parts)
    
    def _build_tone_context(self, primary_tone: str, secondary_tones: List[str]) -> str:
        """Build comprehensive tone context."""
        context_parts = [f"Primary Tone: {primary_tone}"]
        
        if secondary_tones:
            context_parts.append(f"Secondary Tones: {', '.join(secondary_tones)}")
        
        return "\n".join(context_parts)
    
    def _build_market_context(self, industries: List[str], technologies: List[str], business_types: List[str]) -> str:
        """Build comprehensive market context."""
        context_parts = []
        
        if industries:
            context_parts.append(f"Industries: {', '.join(industries)}")
        
        if technologies:
            context_parts.append(f"Technologies: {', '.join(technologies)}")
        
        if business_types:
            context_parts.append(f"Business Types: {', '.join(business_types)}")
        
        if not context_parts:
            context_parts.append("General business market")
        
        return "\n".join(context_parts)
    
    def _build_action_context(self, industries: List[str], market_characteristics: List[str]) -> str:
        """Build action-oriented context for CTA generation."""
        context_parts = []
        
        if industries:
            context_parts.append(f"Target Industries: {', '.join(industries)}")
        
        if market_characteristics:
            relevant_characteristics = [char for char in market_characteristics 
                                      if any(keyword in char.lower() for keyword in ['competitive', 'high', 'tech', 'fast'])]
            if relevant_characteristics:
                context_parts.append(f"Market Type: {', '.join(relevant_characteristics[:2])}")
        
        if not context_parts:
            context_parts.append("General business market")
        
        return "\n".join(context_parts)
    
    def _get_hashtag_style(self, primary_tone: str) -> str:
        """Get hashtag style based on tone."""
        styles = {
            "local": "Mix of local community hashtags and industry-specific ones",
            "corporate": "Professional, industry-focused hashtags with business terminology",
            "technical": "Technology and innovation-focused hashtags with technical terms",
            "professional": "Balanced mix of industry and professional hashtags",
            "casual": "Conversational and approachable hashtags",
            "formal": "Sophisticated and polished hashtags"
        }
        return styles.get(primary_tone, styles["professional"])
    
    def _get_cta_style(self, primary_tone: str) -> str:
        """Get CTA style based on tone."""
        styles = {
            "local": "Friendly and personal, emphasizing local connection",
            "corporate": "Professional and authoritative, emphasizing expertise",
            "technical": "Precise and action-oriented, emphasizing results",
            "professional": "Clear and trustworthy, emphasizing value",
            "casual": "Relaxed and approachable, emphasizing ease",
            "formal": "Polished and sophisticated, emphasizing exclusivity"
        }
        return styles.get(primary_tone, styles["professional"])
    
    def _build_offer_context(self, offer_type: str) -> str:
        """Build offer type context for prompts."""
        offer_descriptions = {
            "discount": "IMPORTANT: This is a DISCOUNT or SALE ad. The ad MUST prominently feature discount/sale language, pricing, savings, or special offers. Use words like 'sale', 'discount', 'save', 'special price', 'deal', 'off', '% off', etc.",
            "promotion": "IMPORTANT: This is a SPECIAL PROMOTION ad. The ad MUST highlight promotional offers, limited-time deals, or special incentives.",
            "free_trial": "IMPORTANT: This is a FREE TRIAL ad. The ad MUST emphasize the free trial offer and encourage users to try the service/product for free.",
            "limited_time": "IMPORTANT: This is a LIMITED TIME OFFER ad. The ad MUST create urgency with time-sensitive language like 'limited time', 'act now', 'ends soon', 'don't miss out', etc.",
            "new_arrival": "IMPORTANT: This is a NEW ARRIVAL or LAUNCH ad. The ad MUST highlight new products, services, or features that are just arriving or launching.",
            "event": "IMPORTANT: This is an EVENT or GRAND OPENING ad. The ad MUST focus on the event, grand opening, or special occasion with event-specific details.",
            "information": "This is an informational ad focusing on brand awareness and information sharing."
        }
        
        description = offer_descriptions.get(offer_type, "")
        if description:
            return f"\n\nOFFER TYPE: {description}"
        return ""

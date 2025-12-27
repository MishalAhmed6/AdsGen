"""
AI Generation Layer Module

A flexible AI-powered content generation system that creates marketing content
from processed context data. Supports multiple LLM providers with easy swapping.

Features:
- Short catchy headlines
- Main ad text generation
- Hashtag creation (3-5 hashtags)
- Call-to-action (CTA) lines
- Provider-agnostic architecture
- Gemini Flash integration
- Template-based prompt engineering
- Content validation and quality scoring
"""

from .core.ai_generation_layer import AIGenerationLayer
from .providers.gemini_provider import GeminiProvider
from .models.content_types import GeneratedContent, ContentPiece, ContentQuality
from .templates.prompt_templates import PromptTemplates
from .exceptions import AIGenerationError, ProviderError, ContentValidationError

__version__ = "1.0.0"
__all__ = [
    "AIGenerationLayer",
    "GeminiProvider",
    "GeneratedContent",
    "ContentPiece",
    "ContentQuality",
    "PromptTemplates",
    "AIGenerationError",
    "ProviderError",
    "ContentValidationError"
]

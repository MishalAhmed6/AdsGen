"""
Data type definitions for AI Generation Layer content.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class ContentType(Enum):
    """Types of generated content."""
    HEADLINE = "headline"
    AD_TEXT = "ad_text"
    HASHTAGS = "hashtags"
    CTA = "cta"


class ContentStatus(Enum):
    """Status of generated content."""
    GENERATED = "generated"
    VALIDATED = "validated"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


@dataclass
class ContentPiece:
    """Individual piece of generated content."""
    content_type: ContentType
    content: str
    status: ContentStatus = ContentStatus.GENERATED
    quality_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    generation_timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "content_type": self.content_type.value,
            "content": self.content,
            "status": self.status.value,
            "quality_score": self.quality_score,
            "metadata": self.metadata,
            "generation_timestamp": self.generation_timestamp
        }


@dataclass
class ContentQuality:
    """Quality metrics for generated content."""
    readability_score: float = 0.0
    engagement_score: float = 0.0
    brand_alignment_score: float = 0.0
    tone_consistency_score: float = 0.0
    length_appropriateness: float = 0.0
    overall_score: float = 0.0
    quality_issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def calculate_overall_score(self) -> float:
        """Calculate overall quality score."""
        scores = [
            self.readability_score,
            self.engagement_score,
            self.brand_alignment_score,
            self.tone_consistency_score,
            self.length_appropriateness
        ]
        self.overall_score = sum(scores) / len(scores) if scores else 0.0
        return self.overall_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "readability_score": self.readability_score,
            "engagement_score": self.engagement_score,
            "brand_alignment_score": self.brand_alignment_score,
            "tone_consistency_score": self.tone_consistency_score,
            "length_appropriateness": self.length_appropriateness,
            "overall_score": self.overall_score,
            "quality_issues": self.quality_issues,
            "suggestions": self.suggestions
        }


@dataclass
class GeneratedContent:
    """Complete set of generated marketing content."""
    headline: ContentPiece
    ad_text: ContentPiece
    hashtags: List[ContentPiece]
    cta: ContentPiece
    overall_quality: ContentQuality
    generation_metadata: Dict[str, Any] = field(default_factory=dict)
    processing_timestamp: Optional[str] = None
    
    def __post_init__(self):
        """Set processing timestamp if not provided."""
        if not self.processing_timestamp:
            self.processing_timestamp = datetime.now().isoformat()
    
    def get_all_content(self) -> List[ContentPiece]:
        """Get all content pieces as a list."""
        return [self.headline, self.ad_text, self.cta] + self.hashtags
    
    def get_content_by_type(self, content_type: ContentType) -> Optional[ContentPiece]:
        """Get content piece by type."""
        if content_type == ContentType.HEADLINE:
            return self.headline
        elif content_type == ContentType.AD_TEXT:
            return self.ad_text
        elif content_type == ContentType.CTA:
            return self.cta
        elif content_type == ContentType.HASHTAGS:
            return self.hashtags[0] if self.hashtags else None
        return None
    
    def get_hashtags_text(self) -> str:
        """Get hashtags as a single string."""
        return " ".join([hashtag.content for hashtag in self.hashtags])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "headline": self.headline.to_dict(),
            "ad_text": self.ad_text.to_dict(),
            "hashtags": [hashtag.to_dict() for hashtag in self.hashtags],
            "hashtags_text": self.get_hashtags_text(),
            "cta": self.cta.to_dict(),
            "overall_quality": self.overall_quality.to_dict(),
            "generation_metadata": self.generation_metadata,
            "processing_timestamp": self.processing_timestamp,
            "summary": self.generate_summary()
        }
    
    def generate_summary(self) -> str:
        """Generate a human-readable summary of the content."""
        summary_parts = []
        
        # Headline
        summary_parts.append(f"Headline: \"{self.headline.content}\"")
        
        # Ad text preview (first 100 chars)
        ad_preview = self.ad_text.content[:100] + "..." if len(self.ad_text.content) > 100 else self.ad_text.content
        summary_parts.append(f"Ad Text: \"{ad_preview}\"")
        
        # Hashtags
        hashtags_text = self.get_hashtags_text()
        summary_parts.append(f"Hashtags: {hashtags_text}")
        
        # CTA
        summary_parts.append(f"CTA: \"{self.cta.content}\"")
        
        # Quality
        summary_parts.append(f"Quality Score: {self.overall_quality.overall_score:.2f}")
        
        return " | ".join(summary_parts)

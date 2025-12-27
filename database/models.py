"""
Database models for campaigns, ads, recipients, and analytics.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import json


class SendStatus(str, Enum):
    """Status of a send operation."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    BOUNCED = "bounced"


class EventType(str, Enum):
    """Types of events to track."""
    SEND = "send"
    DELIVERY = "delivery"
    OPEN = "open"
    CLICK = "click"
    BOUNCE = "bounce"
    FAILURE = "failure"


class Campaign:
    """Campaign model."""
    
    def __init__(self, id: Optional[int] = None, name: Optional[str] = None,
                 brand_name: str = "", competitor_name: str = "",
                 zipcode: str = "", industry: Optional[str] = None,
                 audience_type: Optional[str] = None, offer_type: Optional[str] = None,
                 goal: Optional[str] = None, scheduled_at: Optional[datetime] = None,
                 timezone: Optional[str] = None, status: str = "draft",
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.brand_name = brand_name
        self.competitor_name = competitor_name
        self.zipcode = zipcode
        self.industry = industry
        self.audience_type = audience_type
        self.offer_type = offer_type
        self.goal = goal
        self.scheduled_at = scheduled_at
        self.timezone = timezone
        self.status = status  # draft, scheduled, sending, completed, cancelled
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'brand_name': self.brand_name,
            'competitor_name': self.competitor_name,
            'zipcode': self.zipcode,
            'industry': self.industry,
            'audience_type': self.audience_type,
            'offer_type': self.offer_type,
            'goal': self.goal,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'timezone': self.timezone,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Campaign':
        """Create from dictionary."""
        scheduled_at = datetime.fromisoformat(data['scheduled_at']) if data.get('scheduled_at') else None
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        updated_at = datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            brand_name=data.get('brand_name', ''),
            competitor_name=data.get('competitor_name', ''),
            zipcode=data.get('zipcode', ''),
            industry=data.get('industry'),
            audience_type=data.get('audience_type'),
            offer_type=data.get('offer_type'),
            goal=data.get('goal'),
            scheduled_at=scheduled_at,
            timezone=data.get('timezone'),
            status=data.get('status', 'draft'),
            created_at=created_at,
            updated_at=updated_at
        )


class AdVariant:
    """Ad variant model."""
    
    def __init__(self, id: Optional[int] = None, campaign_id: int = 0,
                 headline: str = "", ad_text: str = "", cta: str = "",
                 hashtags: list = None, quality_score: Optional[float] = None,
                 created_at: Optional[datetime] = None):
        self.id = id
        self.campaign_id = campaign_id
        self.headline = headline
        self.ad_text = ad_text
        self.cta = cta
        self.hashtags = hashtags or []
        self.quality_score = quality_score
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'headline': self.headline,
            'ad_text': self.ad_text,
            'cta': self.cta,
            'hashtags': json.dumps(self.hashtags) if isinstance(self.hashtags, list) else self.hashtags,
            'quality_score': self.quality_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdVariant':
        """Create from dictionary."""
        hashtags = data.get('hashtags', '[]')
        if isinstance(hashtags, str):
            hashtags = json.loads(hashtags)
        
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        
        return cls(
            id=data.get('id'),
            campaign_id=data.get('campaign_id', 0),
            headline=data.get('headline', ''),
            ad_text=data.get('ad_text', ''),
            cta=data.get('cta', ''),
            hashtags=hashtags,
            quality_score=data.get('quality_score'),
            created_at=created_at
        )


class Recipient:
    """Recipient model."""
    
    def __init__(self, id: Optional[int] = None, campaign_id: int = 0,
                 name: str = "", email: Optional[str] = None,
                 phone: Optional[str] = None, channel: str = "",
                 tags: list = None, created_at: Optional[datetime] = None):
        self.id = id
        self.campaign_id = campaign_id
        self.name = name
        self.email = email
        self.phone = phone
        self.channel = channel  # 'sms' or 'email'
        self.tags = tags or []
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'channel': self.channel,
            'tags': json.dumps(self.tags) if isinstance(self.tags, list) else self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recipient':
        """Create from dictionary."""
        tags = data.get('tags', '[]')
        if isinstance(tags, str):
            tags = json.loads(tags)
        
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        
        return cls(
            id=data.get('id'),
            campaign_id=data.get('campaign_id', 0),
            name=data.get('name', ''),
            email=data.get('email'),
            phone=data.get('phone'),
            channel=data.get('channel', ''),
            tags=tags,
            created_at=created_at
        )


class Send:
    """Send tracking model."""
    
    def __init__(self, id: Optional[int] = None, campaign_id: int = 0,
                 ad_variant_id: int = 0, recipient_id: int = 0,
                 channel: str = "", status: str = SendStatus.PENDING,
                 sent_at: Optional[datetime] = None, delivered_at: Optional[datetime] = None,
                 error_message: Optional[str] = None, created_at: Optional[datetime] = None):
        self.id = id
        self.campaign_id = campaign_id
        self.ad_variant_id = ad_variant_id
        self.recipient_id = recipient_id
        self.channel = channel  # 'sms' or 'email'
        self.status = status
        self.sent_at = sent_at
        self.delivered_at = delivered_at
        self.error_message = error_message
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'ad_variant_id': self.ad_variant_id,
            'recipient_id': self.recipient_id,
            'channel': self.channel,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Event:
    """Event tracking model for analytics."""
    
    def __init__(self, id: Optional[int] = None, send_id: int = 0,
                 event_type: str = EventType.SEND, event_data: Dict[str, Any] = None,
                 created_at: Optional[datetime] = None):
        self.id = id
        self.send_id = send_id
        self.event_type = event_type
        self.event_data = event_data or {}
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'send_id': self.send_id,
            'event_type': self.event_type.value if isinstance(self.event_type, Enum) else self.event_type,
            'event_data': json.dumps(self.event_data) if isinstance(self.event_data, dict) else self.event_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


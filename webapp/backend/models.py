"""Pydantic request/response models."""
from typing import Optional, List
from pydantic import BaseModel


class DiscoveryRequest(BaseModel):
    niche: str  # "Beauty", "Fashion", "Fitness", "Finance", "Lifestyle", "Education"
    platform: str  # "YouTube", "Instagram", "Both"
    target_count: int = 50
    country: str = "India"


class InfluencerProfile(BaseModel):
    id: int
    name: str
    handle: str
    platform: str
    followers: int
    engagement_rate: float
    niche: str
    city: str
    content_themes: List[str]
    recent_post_topic: str
    contact_email: str
    profile_url: str
    brand_fit_score: int
    language: str
    source: str = "generated"
    # enriched fields (optional)
    estimated_reach: Optional[int] = None
    tier: Optional[str] = None
    collaboration_score: Optional[float] = None
    outreach_priority: Optional[str] = None


class FilterRequest(BaseModel):
    min_engagement: float = 2.0
    max_engagement: float = 8.5
    min_brand_fit: int = 5
    platforms: List[str] = []
    niches: List[str] = []
    cities: List[str] = []


class MessageRequest(BaseModel):
    influencer_id: int
    collaboration_type: str = "Paid Sponsorship"
    brand_name: str = "Conversely AI Private Limited"


class MessageResponse(BaseModel):
    influencer_id: int
    name: str
    handle: str
    email: str
    email_pitch: str
    dm_pitch: str
    outreach_priority: str
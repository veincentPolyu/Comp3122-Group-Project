from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class Coordinates(BaseModel):
    lat: float
    lng: float

class ContentSource(BaseModel):
    url: str
    type: str  # 'blog', 'video', 'social'
    title: Optional[str]
    timestamp: Optional[str]

class Location(BaseModel):
    id: str = Field(default_factory=str)
    name: str
    address: str
    category: str
    coordinates: Coordinates
    business_hours: Optional[List[str]]
    busy_periods: Optional[List[str]]
    rating: Optional[float]
    price_level: Optional[int]
    photos: Optional[List[str]]
    description: Optional[str]
    source: Optional[ContentSource]
    tags: Optional[List[str]]
    created_at: datetime = Field(default_factory=datetime.utcnow)

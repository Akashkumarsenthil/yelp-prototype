from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RestaurantCreate(BaseModel):
    name: str
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    hours_of_operation: Optional[str] = None
    pricing_tier: Optional[str] = None
    amenities: Optional[str] = None
    ambiance: Optional[str] = None


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    hours_of_operation: Optional[str] = None
    pricing_tier: Optional[str] = None
    amenities: Optional[str] = None
    ambiance: Optional[str] = None


class PhotoOut(BaseModel):
    id: int
    photo_url: str

    class Config:
        from_attributes = True


class RestaurantOut(BaseModel):
    id: int
    name: str
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    hours_of_operation: Optional[str] = None
    pricing_tier: Optional[str] = None
    amenities: Optional[str] = None
    ambiance: Optional[str] = None
    average_rating: float = 0.0
    review_count: int = 0
    owner_id: Optional[int] = None
    created_by: int
    photos: List[PhotoOut] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RestaurantSearch(BaseModel):
    name: Optional[str] = None
    cuisine_type: Optional[str] = None
    keywords: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None

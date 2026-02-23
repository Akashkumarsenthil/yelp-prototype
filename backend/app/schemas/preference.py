from pydantic import BaseModel
from typing import Optional, List


class PreferenceUpdate(BaseModel):
    cuisine_preferences: Optional[List[str]] = None
    price_range: Optional[str] = None
    preferred_locations: Optional[List[str]] = None
    search_radius: Optional[int] = None
    dietary_needs: Optional[List[str]] = None
    ambiance_preferences: Optional[List[str]] = None
    sort_preference: Optional[str] = None


class PreferenceOut(BaseModel):
    id: int
    user_id: int
    cuisine_preferences: Optional[str] = None
    price_range: Optional[str] = None
    preferred_locations: Optional[str] = None
    search_radius: Optional[int] = None
    dietary_needs: Optional[str] = None
    ambiance_preferences: Optional[str] = None
    sort_preference: Optional[str] = None

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    response: str
    restaurants: Optional[List[dict]] = []

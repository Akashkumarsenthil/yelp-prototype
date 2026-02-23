from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    cuisine_preferences = Column(Text, nullable=True)  # JSON string
    price_range = Column(String(20), nullable=True)
    preferred_locations = Column(Text, nullable=True)
    search_radius = Column(Integer, nullable=True)  # in miles
    dietary_needs = Column(Text, nullable=True)  # JSON string
    ambiance_preferences = Column(Text, nullable=True)  # JSON string
    sort_preference = Column(String(50), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preferences")

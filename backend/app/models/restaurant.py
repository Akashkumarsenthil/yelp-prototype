from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    cuisine_type = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(10), nullable=True)
    zip_code = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    hours_of_operation = Column(Text, nullable=True)
    pricing_tier = Column(String(10), nullable=True)  # $, $$, $$$, $$$$
    amenities = Column(Text, nullable=True)
    ambiance = Column(String(100), nullable=True)
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="owned_restaurants", foreign_keys=[owner_id])
    creator = relationship("User", foreign_keys=[created_by])
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")
    favourites = relationship("Favourite", back_populates="restaurant", cascade="all, delete-orphan")
    photos = relationship("RestaurantPhoto", back_populates="restaurant", cascade="all, delete-orphan")

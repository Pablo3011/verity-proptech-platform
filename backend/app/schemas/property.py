"""Property Schemas"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.property import PropertyType, PropertyStatus


class PropertyBase(BaseModel):
    """Base property schema"""
    title: str
    description: Optional[str] = None
    property_type: PropertyType
    country: str
    city: str
    area: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[float] = None
    price: float


class PropertyCreate(PropertyBase):
    """Schema for creating a property"""
    developer_name: Optional[str] = None
    features: Optional[List[str]] = []
    images: Optional[List[str]] = []


class PropertyUpdate(BaseModel):
    """Schema for updating a property"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[PropertyStatus] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None


class Property(PropertyBase):
    """Schema for property response"""
    id: int
    status: PropertyStatus
    developer_name: Optional[str] = None
    views: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PropertySearch(BaseModel):
    """Schema for property search filters"""
    country: Optional[str] = None
    city: Optional[str] = None
    property_type: Optional[PropertyType] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    skip: int = 0
    limit: int = 20

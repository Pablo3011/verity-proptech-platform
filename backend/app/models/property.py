"""Property Models"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum

from app.database import Base


class PropertyType(str, Enum):
    """Property type enumeration"""
    APARTMENT = "apartment"
    VILLA = "villa"
    TOWNHOUSE = "townhouse"
    PENTHOUSE = "penthouse"
    LAND = "land"
    COMMERCIAL = "commercial"


class PropertyStatus(str, Enum):
    """Property status enumeration"""
    AVAILABLE = "available"
    SOLD = "sold"
    RESERVED = "reserved"
    OFF_MARKET = "off_market"


class Property(Base):
    """Property database model"""
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    property_type = Column(SQLEnum(PropertyType), nullable=False)
    status = Column(SQLEnum(PropertyStatus), default=PropertyStatus.AVAILABLE)
    
    # Location
    country = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    area = Column(String)
    address = Column(String)
    
    # Details
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    area_sqft = Column(Float)
    price = Column(Float, nullable=False, index=True)
    
    # Features
    features = Column(Text)  # JSON string
    images = Column(Text)  # JSON string of image URLs
    
    # Developer
    developer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    developer_name = Column(String)
    
    # Metadata
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PropertyValuation(Base):
    """Property valuation model"""
    __tablename__ = "property_valuations"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Valuation data
    estimated_value = Column(Float, nullable=False)
    confidence_score = Column(Float)  # 0-100
    valuation_method = Column(String)  # AI, Comparative, Professional
    
    # Analysis
    market_analysis = Column(Text)  # JSON string
    comparable_properties = Column(Text)  # JSON string
    
    created_at = Column(DateTime, default=datetime.utcnow)

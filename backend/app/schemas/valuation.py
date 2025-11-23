"""Valuation Schemas"""

from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class ValuationRequest(BaseModel):
    """Schema for requesting a property valuation"""
    property_id: int
    valuation_method: str = "AI"  # AI, Comparative, Professional


class Valuation(BaseModel):
    """Schema for valuation response"""
    id: int
    property_id: int
    estimated_value: float
    confidence_score: Optional[float] = None
    valuation_method: str
    market_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

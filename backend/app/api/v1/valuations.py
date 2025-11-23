"""Property Valuation Endpoints"""

import json
import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.property import Property, PropertyValuation
from app.schemas.valuation import ValuationRequest, Valuation as ValuationSchema

router = APIRouter()


@router.post("/", response_model=ValuationSchema, status_code=status.HTTP_201_CREATED)
async def create_valuation(
    valuation_data: ValuationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new property valuation using AI"""
    # Get property
    result = await db.execute(select(Property).where(Property.id == valuation_data.property_id))
    property_obj = result.scalar_one_or_none()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    
    # Perform AI valuation (simplified for now)
    # In production, this would call an ML model or external API
    base_price = property_obj.price
    market_variance = random.uniform(-0.05, 0.10)  # -5% to +10%
    estimated_value = base_price * (1 + market_variance)
    confidence_score = random.uniform(75, 95)
    
    market_analysis = {
        "market_trend": "increasing" if market_variance > 0 else "stable",
        "comparable_properties_count": random.randint(5, 15),
        "price_per_sqft": round(estimated_value / property_obj.area_sqft, 2) if property_obj.area_sqft else None,
        "location_score": random.uniform(70, 95),
    }
    
    # Create valuation record
    db_valuation = PropertyValuation(
        property_id=property_obj.id,
        user_id=1,  # TODO: Get from authenticated user
        estimated_value=round(estimated_value, 2),
        confidence_score=round(confidence_score, 2),
        valuation_method=valuation_data.valuation_method,
        market_analysis=json.dumps(market_analysis),
        comparable_properties=json.dumps([]),
    )
    
    db.add(db_valuation)
    await db.commit()
    await db.refresh(db_valuation)
    
    return db_valuation


@router.get("/property/{property_id}", response_model=List[ValuationSchema])
async def get_property_valuations(
    property_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get all valuations for a specific property"""
    query = (
        select(PropertyValuation)
        .where(PropertyValuation.property_id == property_id)
        .order_by(PropertyValuation.created_at.desc())
    )
    
    result = await db.execute(query)
    valuations = result.scalars().all()
    
    return valuations


@router.get("/{valuation_id}", response_model=ValuationSchema)
async def get_valuation(
    valuation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific valuation by ID"""
    result = await db.execute(
        select(PropertyValuation).where(PropertyValuation.id == valuation_id)
    )
    valuation = result.scalar_one_or_none()
    
    if not valuation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Valuation not found",
        )
    
    return valuation

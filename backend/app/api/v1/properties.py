"""Property Management Endpoints"""

import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models.property import Property, PropertyType, PropertyStatus
from app.schemas.property import PropertyCreate, Property as PropertySchema, PropertyUpdate, PropertySearch

router = APIRouter()


@router.post("/", response_model=PropertySchema, status_code=status.HTTP_201_CREATED)
async def create_property(property_data: PropertyCreate, db: AsyncSession = Depends(get_db)):
    """Create a new property listing"""
    db_property = Property(
        title=property_data.title,
        description=property_data.description,
        property_type=property_data.property_type,
        country=property_data.country,
        city=property_data.city,
        area=property_data.area,
        bedrooms=property_data.bedrooms,
        bathrooms=property_data.bathrooms,
        area_sqft=property_data.area_sqft,
        price=property_data.price,
        developer_name=property_data.developer_name,
        features=json.dumps(property_data.features) if property_data.features else None,
        images=json.dumps(property_data.images) if property_data.images else None,
    )
    
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    
    return db_property


@router.get("/", response_model=List[PropertySchema])
async def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    country: str = None,
    city: str = None,
    property_type: PropertyType = None,
    min_price: float = None,
    max_price: float = None,
    bedrooms: int = None,
    db: AsyncSession = Depends(get_db),
):
    """List properties with optional filters"""
    query = select(Property).where(Property.status == PropertyStatus.AVAILABLE)
    
    # Apply filters
    if country:
        query = query.where(Property.country == country)
    if city:
        query = query.where(Property.city == city)
    if property_type:
        query = query.where(Property.property_type == property_type)
    if min_price is not None:
        query = query.where(Property.price >= min_price)
    if max_price is not None:
        query = query.where(Property.price <= max_price)
    if bedrooms is not None:
        query = query.where(Property.bedrooms == bedrooms)
    
    # Add pagination and ordering
    query = query.order_by(Property.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    properties = result.scalars().all()
    
    return properties


@router.get("/featured", response_model=List[PropertySchema])
async def get_featured_properties(limit: int = Query(6, ge=1, le=20), db: AsyncSession = Depends(get_db)):
    """Get featured properties (most viewed or newest)"""
    query = (
        select(Property)
        .where(Property.status == PropertyStatus.AVAILABLE)
        .order_by(Property.views.desc(), Property.created_at.desc())
        .limit(limit)
    )
    
    result = await db.execute(query)
    properties = result.scalars().all()
    
    return properties


@router.get("/{property_id}", response_model=PropertySchema)
async def get_property(property_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific property by ID"""
    result = await db.execute(select(Property).where(Property.id == property_id))
    property_obj = result.scalar_one_or_none()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    
    # Increment view count
    property_obj.views += 1
    await db.commit()
    await db.refresh(property_obj)
    
    return property_obj


@router.patch("/{property_id}", response_model=PropertySchema)
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a property"""
    result = await db.execute(select(Property).where(Property.id == property_id))
    property_obj = result.scalar_one_or_none()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    
    # Update fields
    update_data = property_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(property_obj, field, value)
    
    await db.commit()
    await db.refresh(property_obj)
    
    return property_obj


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(property_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a property"""
    result = await db.execute(select(Property).where(Property.id == property_id))
    property_obj = result.scalar_one_or_none()
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found",
        )
    
    await db.delete(property_obj)
    await db.commit()
    
    return None


@router.post("/search", response_model=List[PropertySchema])
async def search_properties(search_params: PropertySearch, db: AsyncSession = Depends(get_db)):
    """Advanced property search with multiple filters"""
    query = select(Property).where(Property.status == PropertyStatus.AVAILABLE)
    
    # Apply all search filters
    if search_params.country:
        query = query.where(Property.country == search_params.country)
    if search_params.city:
        query = query.where(Property.city == search_params.city)
    if search_params.property_type:
        query = query.where(Property.property_type == search_params.property_type)
    if search_params.min_price is not None:
        query = query.where(Property.price >= search_params.min_price)
    if search_params.max_price is not None:
        query = query.where(Property.price <= search_params.max_price)
    if search_params.bedrooms is not None:
        query = query.where(Property.bedrooms == search_params.bedrooms)
    if search_params.bathrooms is not None:
        query = query.where(Property.bathrooms == search_params.bathrooms)
    if search_params.min_area is not None:
        query = query.where(Property.area_sqft >= search_params.min_area)
    if search_params.max_area is not None:
        query = query.where(Property.area_sqft <= search_params.max_area)
    
    # Add pagination
    query = query.order_by(Property.created_at.desc()).offset(search_params.skip).limit(search_params.limit)
    
    result = await db.execute(query)
    properties = result.scalars().all()
    
    return properties

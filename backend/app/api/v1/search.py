"""Property Search Endpoints - Real data aggregation"""

from typing import Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.services.property_aggregator import PropertyAggregatorService

router = APIRouter()
aggregator = PropertyAggregatorService()


class PropertySearchRequest(BaseModel):
    """Property search request schema"""
    location: str
    property_type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None


@router.post("/search")
async def search_properties(search_params: PropertySearchRequest):
    """Search properties across Zillow, Realtor.com, and other sources"""
    
    properties = await aggregator.search_properties(
        location=search_params.location,
        property_type=search_params.property_type,
        min_price=search_params.min_price,
        max_price=search_params.max_price,
        bedrooms=search_params.bedrooms,
        bathrooms=search_params.bathrooms,
    )
    
    return {
        "success": True,
        "count": len(properties),
        "properties": properties,
        "sources": list(set(p["source"] for p in properties)),
    }


@router.get("/property-details/{source}/{external_id}")
async def get_property_details(source: str, external_id: str):
    """Get detailed property information from external source"""
    
    details = await aggregator.fetch_property_details(source, external_id)
    
    if not details:
        return {
            "success": False,
            "error": "Property not found",
        }
    
    return {
        "success": True,
        "property": details,
    }


@router.get("/voice-search")
async def voice_search_properties(
    query: str = Query(..., description="Voice search query"),
):
    """Voice-powered property search with NLP"""
    
    # Parse natural language query
    # Example: "3 bedroom villa in Dubai under 2 million"
    # In production, use NLP to extract parameters
    
    # For now, simple keyword extraction
    location = "Dubai" if "dubai" in query.lower() else "UAE"
    
    properties = await aggregator.search_properties(
        location=location,
        property_type=None,
        min_price=None,
        max_price=None,
    )
    
    return {
        "success": True,
        "query": query,
        "interpreted_params": {
            "location": location,
        },
        "count": len(properties),
        "properties": properties[:10],  # Top 10 results
    }


@router.post("/image-search")
async def image_search_properties():
    """Image-based property search (upload image to find similar)"""
    
    # In production, use computer vision to analyze uploaded image
    # and find similar properties
    
    return {
        "success": True,
        "message": "Image search - Upload an image to find similar properties",
        "status": "Feature coming soon - requires image upload integration",
    }

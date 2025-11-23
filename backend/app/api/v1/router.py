"""Main API Router - Updated with all services"""

from fastapi import APIRouter

from app.api.v1 import auth, properties, valuations, health, search, ai_services

api_router = APIRouter()

# Core endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Property management
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(valuations.router, prefix="/valuations", tags=["valuations"])

# Real property search with aggregation
api_router.include_router(search.router, prefix="/search", tags=["property-search"])

# AI-powered services
api_router.include_router(ai_services.router, prefix="/ai", tags=["ai-services"])

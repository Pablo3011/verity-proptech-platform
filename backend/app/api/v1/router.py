"""Main API Router"""

from fastapi import APIRouter

from app.api.v1 import auth, properties, valuations, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(valuations.router, prefix="/valuations", tags=["valuations"])

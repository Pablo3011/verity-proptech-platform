from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="VERITY API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Property(BaseModel):
    id: int
    title: str
    location: str
    price: str
    type: str
    bedrooms: int
    bathrooms: int
    area: int
    status: str
    image: Optional[str] = None
    country: str
    city: str
    developer: Optional[str] = None

class PropertyCreate(BaseModel):
    title: str
    location: str
    price: str
    type: str
    bedrooms: int
    bathrooms: int
    area: int
    description: Optional[str] = None

class ValuationRequest(BaseModel):
    address: str
    property_type: str
    area: int
    bedrooms: int
    bathrooms: Optional[int] = 2

class ValuationResponse(BaseModel):
    estimated_value: str
    confidence: str
    comparable_properties: int
    market_trend: str

# Sample Data - GCC Properties
properties_db = [
    {
        "id": 1,
        "title": "Luxury 3BR Apartment",
        "location": "Dubai Marina, Dubai",
        "price": "AED 2,850,000",
        "type": "apartment",
        "bedrooms": 3,
        "bathrooms": 3,
        "area": 2100,
        "status": "Available",
        "country": "UAE",
        "city": "Dubai",
        "developer": "Emaar"
    },
    {
        "id": 2,
        "title": "Modern 4BR Villa",
        "location": "Arabian Ranches, Dubai",
        "price": "AED 4,200,000",
        "type": "villa",
        "bedrooms": 4,
        "bathrooms": 5,
        "area": 3500,
        "status": "Available",
        "country": "UAE",
        "city": "Dubai",
        "developer": "Emaar"
    },
    {
        "id": 3,
        "title": "Penthouse with Sea View",
        "location": "Jumeirah Beach Residence, Dubai",
        "price": "AED 8,500,000",
        "type": "penthouse",
        "bedrooms": 5,
        "bathrooms": 6,
        "area": 5200,
        "status": "Featured",
        "country": "UAE",
        "city": "Dubai",
        "developer": "DAMAC"
    },
    {
        "id": 4,
        "title": "2BR Apartment Downtown",
        "location": "Downtown Dubai",
        "price": "AED 1,950,000",
        "type": "apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1400,
        "status": "New",
        "country": "UAE",
        "city": "Dubai",
        "developer": "Emaar"
    },
    {
        "id": 5,
        "title": "Spacious 5BR Villa",
        "location": "Palm Jumeirah, Dubai",
        "price": "AED 12,000,000",
        "type": "villa",
        "bedrooms": 5,
        "bathrooms": 6,
        "area": 6800,
        "status": "Premium",
        "country": "UAE",
        "city": "Dubai",
        "developer": "Nakheel"
    },
    {
        "id": 6,
        "title": "3BR Townhouse",
        "location": "DAMAC Hills, Dubai",
        "price": "AED 2,100,000",
        "type": "townhouse",
        "bedrooms": 3,
        "bathrooms": 4,
        "area": 2200,
        "status": "Available",
        "country": "UAE",
        "city": "Dubai",
        "developer": "DAMAC"
    },
    {
        "id": 7,
        "title": "Luxury Apartment",
        "location": "West Bay, Doha",
        "price": "QAR 2,500,000",
        "type": "apartment",
        "bedrooms": 3,
        "bathrooms": 3,
        "area": 1800,
        "status": "Available",
        "country": "Qatar",
        "city": "Doha",
        "developer": "Qatari Diar"
    },
    {
        "id": 8,
        "title": "Elegant Villa",
        "location": "The Pearl, Doha",
        "price": "QAR 5,800,000",
        "type": "villa",
        "bedrooms": 5,
        "bathrooms": 6,
        "area": 4500,
        "status": "Premium",
        "country": "Qatar",
        "city": "Doha",
        "developer": "UDC"
    },
    {
        "id": 9,
        "title": "Modern Apartment",
        "location": "Riyadh City, Riyadh",
        "price": "SAR 1,800,000",
        "type": "apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1500,
        "status": "Available",
        "country": "Saudi Arabia",
        "city": "Riyadh"
    },
    {
        "id": 10,
        "title": "Luxury Compound Villa",
        "location": "Jeddah, Saudi Arabia",
        "price": "SAR 4,500,000",
        "type": "villa",
        "bedrooms": 6,
        "bathrooms": 7,
        "area": 5000,
        "status": "Featured",
        "country": "Saudi Arabia",
        "city": "Jeddah"
    },
    {
        "id": 11,
        "title": "Modern 2BR Flat",
        "location": "New Cairo, Cairo",
        "price": "EGP 3,500,000",
        "type": "apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1200,
        "status": "Available",
        "country": "Egypt",
        "city": "Cairo"
    },
    {
        "id": 12,
        "title": "Seaside Villa",
        "location": "North Coast, Egypt",
        "price": "EGP 12,000,000",
        "type": "villa",
        "bedrooms": 4,
        "bathrooms": 5,
        "area": 3800,
        "status": "Premium",
        "country": "Egypt",
        "city": "North Coast"
    }
]

# API Routes
@app.get("/")
async def root():
    return {
        "name": "VERITY API",
        "version": "1.0.0",
        "status": "operational",
        "message": "AI-Powered GCC Real Estate Platform"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "verity-backend"}

@app.get("/api/properties", response_model=List[Property])
async def get_properties(
    type: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    min_bedrooms: Optional[int] = None,
    max_price: Optional[int] = None
):
    """Get all properties with optional filters"""
    filtered = properties_db.copy()
    
    if type:
        filtered = [p for p in filtered if p["type"].lower() == type.lower()]
    
    if country:
        filtered = [p for p in filtered if p["country"].lower() == country.lower()]
    
    if city:
        filtered = [p for p in filtered if city.lower() in p["city"].lower()]
    
    if min_bedrooms:
        filtered = [p for p in filtered if p["bedrooms"] >= min_bedrooms]
    
    return filtered

@app.get("/api/properties/{property_id}", response_model=Property)
async def get_property(property_id: int):
    """Get a specific property by ID"""
    property_item = next((p for p in properties_db if p["id"] == property_id), None)
    
    if not property_item:
        raise HTTPException(status_code=404, detail="Property not found")
    
    return property_item

@app.get("/api/properties/search/{query}")
async def search_properties(query: str):
    """Search properties by location or title"""
    query_lower = query.lower()
    results = [
        p for p in properties_db 
        if query_lower in p["title"].lower() 
        or query_lower in p["location"].lower()
        or query_lower in p.get("city", "").lower()
        or query_lower in p.get("country", "").lower()
    ]
    return results

@app.post("/api/properties", response_model=Property)
async def create_property(property_data: PropertyCreate):
    """Create a new property listing"""
    new_id = max([p["id"] for p in properties_db]) + 1
    
    new_property = {
        "id": new_id,
        "title": property_data.title,
        "location": property_data.location,
        "price": property_data.price,
        "type": property_data.type,
        "bedrooms": property_data.bedrooms,
        "bathrooms": property_data.bathrooms,
        "area": property_data.area,
        "status": "Pending",
        "country": "UAE",
        "city": "Dubai"
    }
    
    properties_db.append(new_property)
    return new_property

@app.post("/api/valuations", response_model=ValuationResponse)
async def get_valuation(valuation_request: ValuationRequest):
    """Get AI-powered property valuation"""
    # Simple valuation logic - in production, this would use ML models
    base_price_per_sqft = 1200  # AED
    estimated_price = valuation_request.area * base_price_per_sqft
    
    # Adjust for property type
    type_multipliers = {
        "apartment": 1.0,
        "villa": 1.3,
        "penthouse": 1.6,
        "townhouse": 1.15
    }
    
    multiplier = type_multipliers.get(valuation_request.property_type.lower(), 1.0)
    estimated_price = int(estimated_price * multiplier)
    
    return ValuationResponse(
        estimated_value=f"AED {estimated_price:,}",
        confidence="High (87%)",
        comparable_properties=42,
        market_trend="Increasing (+5.2% YoY)"
    )

@app.get("/api/stats")
async def get_stats():
    """Get platform statistics"""
    return {
        "total_properties": len(properties_db),
        "active_listings": len([p for p in properties_db if p["status"] in ["Available", "Featured", "New"]]),
        "avg_price": "AED 4,200,000",
        "countries_covered": 4,
        "cities_covered": 8
    }

@app.get("/api/developers")
async def get_developers():
    """Get list of developers"""
    developers = list(set([p.get("developer", "Unknown") for p in properties_db if p.get("developer")]))
    return {"developers": developers}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
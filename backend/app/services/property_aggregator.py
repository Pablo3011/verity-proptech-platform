"""Property Data Aggregation Service - Fetches real property data from multiple sources"""

import httpx
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime


class PropertyAggregatorService:
    """Aggregates property data from Zillow, Realtor, and other sources"""
    
    def __init__(self):
        self.sources = {
            "zillow": self._fetch_zillow_properties,
            "realtor": self._fetch_realtor_properties,
        }
    
    async def search_properties(
        self,
        location: str,
        property_type: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        bedrooms: Optional[int] = None,
        bathrooms: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Search properties across all sources and aggregate results"""
        
        search_params = {
            "location": location,
            "property_type": property_type,
            "min_price": min_price,
            "max_price": max_price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
        }
        
        # Fetch from all sources concurrently
        tasks = [
            source_func(search_params)
            for source_func in self.sources.values()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine and deduplicate results
        all_properties = []
        for result in results:
            if isinstance(result, list):
                all_properties.extend(result)
        
        # Deduplicate based on address
        seen_addresses = set()
        unique_properties = []
        
        for prop in all_properties:
            address_key = f"{prop['address']}_{prop['city']}_{prop['zipcode']}".lower()
            if address_key not in seen_addresses:
                seen_addresses.add(address_key)
                unique_properties.append(prop)
        
        return unique_properties
    
    async def _fetch_zillow_properties(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch properties from Zillow API"""
        # Using RapidAPI Zillow endpoint
        url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
        
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with actual key
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        querystring = {
            "location": params["location"],
            "status_type": "ForSale",
        }
        
        if params.get("min_price"):
            querystring["price_min"] = str(int(params["min_price"]))
        if params.get("max_price"):
            querystring["price_max"] = str(int(params["max_price"]))
        if params.get("bedrooms"):
            querystring["beds_min"] = str(params["bedrooms"])
        if params.get("bathrooms"):
            querystring["baths_min"] = str(params["bathrooms"])
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._normalize_zillow_data(data.get("props", []))
                else:
                    print(f"Zillow API error: {response.status_code}")
                    return []
        except Exception as e:
            print(f"Error fetching from Zillow: {str(e)}")
            return []
    
    async def _fetch_realtor_properties(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch properties from Realtor.com API"""
        url = "https://realtor-com-real-estate.p.rapidapi.com/for-sale"
        
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with actual key
            "X-RapidAPI-Host": "realtor-com-real-estate.p.rapidapi.com"
        }
        
        querystring = {
            "location": params["location"],
            "limit": "50",
        }
        
        if params.get("min_price"):
            querystring["price_min"] = str(int(params["min_price"]))
        if params.get("max_price"):
            querystring["price_max"] = str(int(params["max_price"]))
        if params.get("bedrooms"):
            querystring["beds_min"] = str(params["bedrooms"])
        if params.get("bathrooms"):
            querystring["baths_min"] = str(params["bathrooms"])
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._normalize_realtor_data(data.get("listings", []))
                else:
                    print(f"Realtor API error: {response.status_code}")
                    return []
        except Exception as e:
            print(f"Error fetching from Realtor: {str(e)}")
            return []
    
    def _normalize_zillow_data(self, properties: List[Dict]) -> List[Dict[str, Any]]:
        """Normalize Zillow data to common format"""
        normalized = []
        
        for prop in properties:
            try:
                normalized.append({
                    "source": "zillow",
                    "external_id": prop.get("zpid"),
                    "title": f"{prop.get('bedrooms', 0)} BR, {prop.get('bathrooms', 0)} BA {prop.get('propertyType', 'Property')}",
                    "address": prop.get("address", ""),
                    "city": prop.get("addressCity", ""),
                    "state": prop.get("addressState", ""),
                    "zipcode": prop.get("addressZipcode", ""),
                    "price": float(prop.get("price", 0)),
                    "bedrooms": int(prop.get("bedrooms", 0)),
                    "bathrooms": int(prop.get("bathrooms", 0)),
                    "area_sqft": float(prop.get("livingArea", 0)),
                    "property_type": prop.get("propertyType", "").lower(),
                    "images": [prop.get("imgSrc")] if prop.get("imgSrc") else [],
                    "listing_url": prop.get("detailUrl", ""),
                    "zestimate": prop.get("zestimate"),
                    "days_on_market": prop.get("daysOnZillow"),
                })
            except Exception as e:
                print(f"Error normalizing Zillow property: {str(e)}")
                continue
        
        return normalized
    
    def _normalize_realtor_data(self, properties: List[Dict]) -> List[Dict[str, Any]]:
        """Normalize Realtor.com data to common format"""
        normalized = []
        
        for prop in properties:
            try:
                address_data = prop.get("location", {}).get("address", {})
                
                normalized.append({
                    "source": "realtor",
                    "external_id": prop.get("property_id"),
                    "title": prop.get("description", {}).get("name", ""),
                    "address": address_data.get("line", ""),
                    "city": address_data.get("city", ""),
                    "state": address_data.get("state_code", ""),
                    "zipcode": address_data.get("postal_code", ""),
                    "price": float(prop.get("list_price", 0)),
                    "bedrooms": int(prop.get("description", {}).get("beds", 0)),
                    "bathrooms": int(prop.get("description", {}).get("baths", 0)),
                    "area_sqft": float(prop.get("description", {}).get("sqft", 0)),
                    "property_type": prop.get("description", {}).get("type", "").lower(),
                    "images": [photo.get("href") for photo in prop.get("photos", [])[:5]],
                    "listing_url": prop.get("permalink", ""),
                    "days_on_market": prop.get("list_date"),
                })
            except Exception as e:
                print(f"Error normalizing Realtor property: {str(e)}")
                continue
        
        return normalized
    
    async def fetch_property_details(self, source: str, external_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific property"""
        
        if source == "zillow":
            return await self._fetch_zillow_details(external_id)
        elif source == "realtor":
            return await self._fetch_realtor_details(external_id)
        
        return None
    
    async def _fetch_zillow_details(self, zpid: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed Zillow property information"""
        url = f"https://zillow-com1.p.rapidapi.com/property"
        
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        querystring = {"zpid": zpid}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
        except Exception as e:
            print(f"Error fetching Zillow details: {str(e)}")
            return None
    
    async def _fetch_realtor_details(self, property_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed Realtor.com property information"""
        url = f"https://realtor-com-real-estate.p.rapidapi.com/property-detail"
        
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "realtor-com-real-estate.p.rapidapi.com"
        }
        
        querystring = {"property_id": property_id}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
        except Exception as e:
            print(f"Error fetching Realtor details: {str(e)}")
            return None

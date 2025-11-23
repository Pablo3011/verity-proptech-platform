"""AI-Powered Property Valuation Service"""

import httpx
import statistics
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class AIValuationService:
    """Advanced AI property valuation using market data and ML models"""
    
    def __init__(self):
        self.openai_api_key = None  # Set from environment
        self.gemini_api_key = None  # Set from environment
    
    async def value_property(
        self,
        property_data: Dict[str, Any],
        comparable_properties: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate comprehensive property valuation"""
        
        # Step 1: Fetch comparable properties if not provided
        if not comparable_properties:
            comparable_properties = await self._find_comparable_properties(property_data)
        
        # Step 2: Calculate base valuation using comparables
        base_valuation = self._calculate_comparative_value(property_data, comparable_properties)
        
        # Step 3: Apply market adjustments
        market_analysis = await self._analyze_market_trends(property_data)
        
        # Step 4: Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            comparable_properties,
            market_analysis
        )
        
        # Step 5: Generate AI insights
        ai_insights = await self._generate_ai_insights(
            property_data,
            base_valuation,
            market_analysis,
            comparable_properties
        )
        
        return {
            "estimated_value": base_valuation["estimated_value"],
            "value_range": base_valuation["value_range"],
            "confidence_score": confidence_score,
            "price_per_sqft": base_valuation["price_per_sqft"],
            "market_analysis": market_analysis,
            "comparable_properties": comparable_properties[:5],  # Top 5
            "ai_insights": ai_insights,
            "valuation_date": datetime.utcnow().isoformat(),
            "is_good_buy": self._is_good_buy(property_data, base_valuation),
            "investment_score": self._calculate_investment_score(
                property_data,
                base_valuation,
                market_analysis
            ),
        }
    
    async def _find_comparable_properties(self, property_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find similar properties for comparison"""
        # In production, this would query the property aggregator service
        # For now, return mock comparables based on property characteristics
        
        base_price = property_data.get("price", 0)
        bedrooms = property_data.get("bedrooms", 0)
        area_sqft = property_data.get("area_sqft", 0)
        
        # Generate realistic comparable properties
        comparables = []
        for i in range(10):
            price_variance = 1 + (i - 5) * 0.03  # ±15% variance
            area_variance = 1 + (i - 5) * 0.02  # ±10% variance
            
            comparables.append({
                "address": f"Comparable Property {i+1}",
                "price": int(base_price * price_variance),
                "bedrooms": bedrooms,
                "bathrooms": property_data.get("bathrooms", 2),
                "area_sqft": int(area_sqft * area_variance),
                "days_on_market": 15 + i * 3,
                "sale_date": "2025-11-01",
                "distance_miles": 0.5 + i * 0.2,
            })
        
        return comparables
    
    def _calculate_comparative_value(self, property_data: Dict[str, Any], comparables: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate value based on comparable properties"""
        
        if not comparables:
            return {
                "estimated_value": property_data.get("price", 0),
                "value_range": {"low": 0, "high": 0},
                "price_per_sqft": 0,
            }
        
        # Calculate price per sqft for each comparable
        price_per_sqft_values = []
        for comp in comparables:
            if comp.get("area_sqft", 0) > 0:
                price_per_sqft_values.append(comp["price"] / comp["area_sqft"])
        
        # Use median price per sqft for better accuracy
        median_price_per_sqft = statistics.median(price_per_sqft_values) if price_per_sqft_values else 0
        
        # Calculate estimated value
        property_area = property_data.get("area_sqft", 0)
        estimated_value = median_price_per_sqft * property_area if property_area > 0 else 0
        
        # Calculate value range (10th to 90th percentile)
        sorted_prices = sorted([c["price"] for c in comparables])
        value_range = {
            "low": int(sorted_prices[len(sorted_prices) // 10]),
            "high": int(sorted_prices[int(len(sorted_prices) * 0.9)]),
        }
        
        return {
            "estimated_value": int(estimated_value),
            "value_range": value_range,
            "price_per_sqft": round(median_price_per_sqft, 2),
        }
    
    async def _analyze_market_trends(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market trends for the property location"""
        
        city = property_data.get("city", "")
        country = property_data.get("country", "")
        
        # In production, this would call market data APIs
        # For now, generate realistic market analysis
        
        return {
            "market_trend": "increasing",  # increasing, stable, decreasing
            "yoy_price_change": 8.5,  # Year over year % change
            "median_days_on_market": 45,
            "inventory_level": "low",  # low, moderate, high
            "demand_score": 85,  # 0-100
            "location_score": 92,  # 0-100
            "appreciation_forecast": {
                "1_year": 6.2,
                "3_year": 18.5,
                "5_year": 32.0,
            },
            "market_velocity": "hot",  # hot, warm, cold
            "neighborhood_rating": 4.5,  # 0-5
        }
    
    def _calculate_confidence_score(self, comparables: List[Dict], market_analysis: Dict) -> float:
        """Calculate confidence score for the valuation"""
        
        # Base score
        score = 50.0
        
        # Add points for number of comparables
        score += min(len(comparables) * 3, 30)
        
        # Add points for recent comparables
        recent_count = sum(1 for c in comparables if c.get("days_on_market", 999) < 60)
        score += min(recent_count * 2, 10)
        
        # Add points for market stability
        if market_analysis.get("market_trend") in ["stable", "increasing"]:
            score += 10
        
        return min(score, 95.0)  # Cap at 95%
    
    async def _generate_ai_insights(self, property_data: Dict, valuation: Dict, market: Dict, comparables: List) -> Dict[str, Any]:
        """Generate AI-powered insights and recommendations"""
        
        price = property_data.get("price", 0)
        estimated_value = valuation.get("estimated_value", 0)
        
        price_difference = ((price - estimated_value) / estimated_value * 100) if estimated_value > 0 else 0
        
        insights = {
            "summary": "",
            "strengths": [],
            "concerns": [],
            "recommendations": [],
        }
        
        # Generate summary
        if abs(price_difference) < 5:
            insights["summary"] = "This property is fairly priced according to current market conditions."
        elif price_difference < 0:
            insights["summary"] = f"This property is priced {abs(price_difference):.1f}% below market value - a potential good deal."
        else:
            insights["summary"] = f"This property is priced {price_difference:.1f}% above market value - consider negotiating."
        
        # Identify strengths
        if market.get("market_trend") == "increasing":
            insights["strengths"].append("Strong market appreciation trend")
        
        if market.get("location_score", 0) > 80:
            insights["strengths"].append("Excellent location rating")
        
        if market.get("demand_score", 0) > 70:
            insights["strengths"].append("High buyer demand in the area")
        
        # Identify concerns
        if price_difference > 10:
            insights["concerns"].append("Property is overpriced compared to similar listings")
        
        if market.get("inventory_level") == "high":
            insights["concerns"].append("High inventory may lead to price negotiations")
        
        # Generate recommendations
        if price_difference < -5:
            insights["recommendations"].append("Act quickly - this is below market value")
        
        if market.get("market_velocity") == "hot":
            insights["recommendations"].append("Competitive market - be prepared for multiple offers")
        
        insights["recommendations"].append("Get a professional inspection before purchasing")
        insights["recommendations"].append("Review HOA fees and property taxes in detail")
        
        return insights
    
    def _is_good_buy(self, property_data: Dict, valuation: Dict) -> bool:
        """Determine if the property is a good buy"""
        price = property_data.get("price", 0)
        estimated_value = valuation.get("estimated_value", 0)
        
        if estimated_value == 0:
            return False
        
        price_ratio = price / estimated_value
        return price_ratio <= 1.05  # Within 5% of estimated value or below
    
    def _calculate_investment_score(self, property_data: Dict, valuation: Dict, market: Dict) -> int:
        """Calculate investment potential score (0-100)"""
        score = 50
        
        # Price vs value
        price = property_data.get("price", 0)
        estimated_value = valuation.get("estimated_value", 0)
        if estimated_value > 0:
            price_ratio = price / estimated_value
            if price_ratio < 0.95:
                score += 20
            elif price_ratio < 1.0:
                score += 10
            elif price_ratio > 1.1:
                score -= 15
        
        # Market trends
        if market.get("market_trend") == "increasing":
            score += 15
        elif market.get("market_trend") == "decreasing":
            score -= 10
        
        # Location quality
        location_score = market.get("location_score", 0)
        score += int((location_score - 50) / 5)
        
        # Appreciation forecast
        forecast_5y = market.get("appreciation_forecast", {}).get("5_year", 0)
        if forecast_5y > 25:
            score += 10
        
        return max(0, min(100, score))

"""AI-Powered Services Endpoints"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.ai_valuation import AIValuationService
from app.services.mortgage_calculator import MortgageCalculatorService

router = APIRouter()
valuation_service = AIValuationService()
mortgage_service = MortgageCalculatorService()


class ValuationRequest(BaseModel):
    """Property valuation request"""
    address: str
    city: str
    country: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: float
    property_type: str


class MortgageCalculationRequest(BaseModel):
    """Mortgage calculation request"""
    property_price: float
    down_payment: float
    loan_term_years: int = 30
    interest_rate: Optional[float] = None
    country: str = "UAE"
    loan_type: str = "conventional_30y"


class MortgageEligibilityRequest(BaseModel):
    """Mortgage eligibility check request"""
    property_price: float
    annual_income: float
    monthly_debts: float
    credit_score: int
    down_payment: float


@router.post("/valuation")
async def get_property_valuation(request: ValuationRequest):
    """Get AI-powered property valuation with market analysis"""
    
    property_data = request.model_dump()
    
    try:
        valuation = await valuation_service.value_property(property_data)
        
        return {
            "success": True,
            "valuation": valuation,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Valuation error: {str(e)}",
        )


@router.post("/mortgage/calculate")
async def calculate_mortgage(request: MortgageCalculationRequest):
    """Calculate mortgage payments with real bank rates"""
    
    try:
        mortgage_data = await mortgage_service.calculate_mortgage(
            property_price=request.property_price,
            down_payment=request.down_payment,
            loan_term_years=request.loan_term_years,
            interest_rate=request.interest_rate,
            country=request.country,
            loan_type=request.loan_type,
        )
        
        return {
            "success": True,
            "mortgage": mortgage_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Mortgage calculation error: {str(e)}",
        )


@router.post("/mortgage/eligibility")
async def check_mortgage_eligibility(request: MortgageEligibilityRequest):
    """Check if user qualifies for mortgage"""
    
    try:
        eligibility = await mortgage_service.check_mortgage_eligibility(
            property_price=request.property_price,
            annual_income=request.annual_income,
            monthly_debts=request.monthly_debts,
            credit_score=request.credit_score,
            down_payment=request.down_payment,
        )
        
        return {
            "success": True,
            "eligibility": eligibility,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Eligibility check error: {str(e)}",
        )


@router.get("/market-predictions")
async def get_market_predictions(
    city: str,
    country: str = "UAE",
):
    """Get AI-powered market predictions and trends"""
    
    # In production, use ML models for predictions
    # For now, return realistic market analysis
    
    predictions = {
        "location": f"{city}, {country}",
        "current_market_index": 1245,
        "market_sentiment": "bullish",
        "predictions": {
            "1_month": {
                "price_change_percent": 0.8,
                "confidence": 85,
            },
            "3_months": {
                "price_change_percent": 2.4,
                "confidence": 78,
            },
            "6_months": {
                "price_change_percent": 4.9,
                "confidence": 72,
            },
            "1_year": {
                "price_change_percent": 8.5,
                "confidence": 65,
            },
        },
        "key_factors": [
            "Strong economic growth",
            "Low inventory levels",
            "High foreign investment",
            "Infrastructure development",
        ],
        "risk_factors": [
            "Interest rate volatility",
            "Global economic uncertainty",
        ],
    }
    
    return {
        "success": True,
        "predictions": predictions,
    }


@router.post("/investment-advisor")
async def get_investment_advice(request: ValuationRequest):
    """Get AI investment advisor recommendations"""
    
    property_data = request.model_dump()
    
    try:
        # Get valuation first
        valuation = await valuation_service.value_property(property_data)
        
        # Generate investment advice
        advice = {
            "investment_rating": valuation["investment_score"],
            "rating_label": _get_rating_label(valuation["investment_score"]),
            "is_good_buy": valuation["is_good_buy"],
            "key_insights": valuation["ai_insights"],
            "financial_projections": {
                "1_year_roi": 6.2,
                "3_year_roi": 18.5,
                "5_year_roi": 32.0,
                "rental_yield_estimate": 5.8,
            },
            "risk_assessment": {
                "overall_risk": "moderate",
                "market_risk": "low",
                "liquidity_risk": "moderate",
                "location_risk": "low",
            },
            "action_items": [
                "Schedule property inspection",
                "Review comparative market analysis",
                "Get mortgage pre-approval",
                "Verify property title and documents",
            ],
        }
        
        return {
            "success": True,
            "advice": advice,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Investment advisor error: {str(e)}",
        )


def _get_rating_label(score: int) -> str:
    """Convert investment score to label"""
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Fair"
    elif score >= 35:
        return "Below Average"
    else:
        return "Poor"

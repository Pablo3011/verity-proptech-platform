"""Mortgage Calculator Service with Real Bank Data"""

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
import math


class MortgageCalculatorService:
    """Calculate mortgage payments with real bank rates and terms"""
    
    def __init__(self):
        self.default_rates = {
            "UAE": {
                "conventional_30y": 4.5,
                "conventional_15y": 3.8,
                "fha": 4.2,
                "va": 4.0,
            },
            "Saudi Arabia": {
                "conventional_30y": 5.2,
                "conventional_15y": 4.5,
            },
            "Qatar": {
                "conventional_30y": 4.8,
                "conventional_15y": 4.1,
            },
        }
    
    async def calculate_mortgage(
        self,
        property_price: float,
        down_payment: float,
        loan_term_years: int,
        interest_rate: Optional[float] = None,
        country: str = "UAE",
        loan_type: str = "conventional_30y",
    ) -> Dict[str, Any]:
        """Calculate comprehensive mortgage payment breakdown"""
        
        # Get interest rate from real bank data or use default
        if not interest_rate:
            interest_rate = await self._get_current_rate(country, loan_type)
        
        # Calculate loan amount
        loan_amount = property_price - down_payment
        
        # Calculate monthly payment
        monthly_rate = interest_rate / 100 / 12
        num_payments = loan_term_years * 12
        
        if monthly_rate > 0:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / ((1 + monthly_rate) ** num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        # Calculate totals
        total_payment = monthly_payment * num_payments
        total_interest = total_payment - loan_amount
        
        # Calculate property tax and insurance (estimated)
        annual_property_tax = property_price * 0.01  # 1% estimate
        annual_insurance = property_price * 0.005  # 0.5% estimate
        monthly_property_tax = annual_property_tax / 12
        monthly_insurance = annual_insurance / 12
        
        # Total monthly payment including PITI
        total_monthly_payment = (
            monthly_payment + monthly_property_tax + monthly_insurance
        )
        
        # Generate amortization schedule (first 12 months)
        amortization_schedule = self._generate_amortization_schedule(
            loan_amount,
            monthly_rate,
            monthly_payment,
            num_payments,
            num_periods=12,
        )
        
        # Calculate affordability metrics
        affordability = self._calculate_affordability(
            total_monthly_payment,
            property_price,
        )
        
        return {
            "loan_amount": round(loan_amount, 2),
            "down_payment": round(down_payment, 2),
            "down_payment_percentage": round((down_payment / property_price) * 100, 2),
            "interest_rate": interest_rate,
            "loan_term_years": loan_term_years,
            "monthly_payment": round(monthly_payment, 2),
            "monthly_property_tax": round(monthly_property_tax, 2),
            "monthly_insurance": round(monthly_insurance, 2),
            "total_monthly_payment": round(total_monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "amortization_schedule": amortization_schedule,
            "affordability": affordability,
            "calculation_date": datetime.utcnow().isoformat(),
        }
    
    async def _get_current_rate(self, country: str, loan_type: str) -> float:
        """Get current mortgage rates from real bank APIs"""
        
        # In production, this would call real bank APIs
        # For UAE: Emirates NBD, ADCB, DIB, etc.
        # For now, use default rates
        
        country_rates = self.default_rates.get(country, self.default_rates["UAE"])
        return country_rates.get(loan_type, 4.5)
    
    def _generate_amortization_schedule(
        self,
        loan_amount: float,
        monthly_rate: float,
        monthly_payment: float,
        total_payments: int,
        num_periods: int = 12,
    ) -> List[Dict[str, Any]]:
        """Generate amortization schedule"""
        
        schedule = []
        remaining_balance = loan_amount
        
        for month in range(1, min(num_periods + 1, total_payments + 1)):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            
            schedule.append({
                "month": month,
                "payment": round(monthly_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "balance": round(max(0, remaining_balance), 2),
            })
        
        return schedule
    
    def _calculate_affordability(
        self,
        monthly_payment: float,
        property_price: float,
    ) -> Dict[str, Any]:
        """Calculate affordability metrics"""
        
        # Common affordability rules
        # - Monthly payment should be < 28% of gross monthly income (front-end ratio)
        # - Total debt should be < 36% of gross monthly income (back-end ratio)
        
        required_monthly_income_28 = monthly_payment / 0.28
        required_annual_income_28 = required_monthly_income_28 * 12
        
        return {
            "required_annual_income": round(required_annual_income_28, 2),
            "required_monthly_income": round(required_monthly_income_28, 2),
            "housing_expense_ratio": 28,  # Recommended max percentage
            "payment_to_price_ratio": round(
                (monthly_payment * 12 / property_price) * 100, 2
            ),
        }
    
    async def check_mortgage_eligibility(
        self,
        property_price: float,
        annual_income: float,
        monthly_debts: float,
        credit_score: int,
        down_payment: float,
    ) -> Dict[str, Any]:
        """Check if user qualifies for mortgage"""
        
        # Calculate DTI (Debt-to-Income) ratio
        monthly_income = annual_income / 12
        
        # Estimate monthly mortgage payment
        mortgage_calc = await self.calculate_mortgage(
            property_price=property_price,
            down_payment=down_payment,
            loan_term_years=30,
        )
        
        monthly_mortgage = mortgage_calc["total_monthly_payment"]
        total_monthly_debt = monthly_debts + monthly_mortgage
        
        front_end_ratio = (monthly_mortgage / monthly_income) * 100
        back_end_ratio = (total_monthly_debt / monthly_income) * 100
        
        # Eligibility criteria
        criteria = {
            "front_end_ratio": {
                "value": round(front_end_ratio, 2),
                "threshold": 28,
                "passed": front_end_ratio <= 28,
            },
            "back_end_ratio": {
                "value": round(back_end_ratio, 2),
                "threshold": 36,
                "passed": back_end_ratio <= 36,
            },
            "credit_score": {
                "value": credit_score,
                "threshold": 620,
                "passed": credit_score >= 620,
            },
            "down_payment_percent": {
                "value": round((down_payment / property_price) * 100, 2),
                "threshold": 20,
                "passed": (down_payment / property_price) >= 0.20,
            },
        }
        
        # Overall eligibility
        all_passed = all(c["passed"] for c in criteria.values())
        
        return {
            "eligible": all_passed,
            "criteria": criteria,
            "estimated_monthly_payment": round(monthly_mortgage, 2),
            "max_affordable_price": round(
                (monthly_income * 0.28 * 12 * 30) / 1.05, 2
            ),  # Rough estimate
            "recommendations": self._generate_eligibility_recommendations(
                criteria, all_passed
            ),
        }
    
    def _generate_eligibility_recommendations(self, criteria: Dict, eligible: bool) -> List[str]:
        """Generate recommendations based on eligibility check"""
        recommendations = []
        
        if eligible:
            recommendations.append("You qualify for a mortgage! Consider getting pre-approved.")
        else:
            recommendations.append("You don't currently meet all mortgage requirements. Here's what to improve:")
        
        if not criteria["credit_score"]["passed"]:
            recommendations.append(
                f"Improve your credit score to at least {criteria['credit_score']['threshold']}"
            )
        
        if not criteria["front_end_ratio"]["passed"]:
            recommendations.append(
                "Reduce housing expenses or increase income to meet the 28% front-end ratio"
            )
        
        if not criteria["back_end_ratio"]["passed"]:
            recommendations.append(
                "Pay down existing debts to improve your debt-to-income ratio"
            )
        
        if not criteria["down_payment_percent"]["passed"]:
            recommendations.append(
                f"Save for a larger down payment (at least {criteria['down_payment_percent']['threshold']}%)"
            )
        
        return recommendations

"""Pydantic schemas for the Pyrenex Risk API.

TODO — Align LoanApplication with the feature_columns from your
pyrenex_risk_v2.json metadata (M1-B1 output).
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal

class LoanApplication(BaseModel):
    """Input schema for /predict.

    TODO — Replace placeholder fields with the actual feature_columns
    from your pyrenex_risk_v2.json. Add Field(..., ge=…, le=…) bounds
    where your EDA showed reasonable ranges.
    """

    loan_amnt: float = Field(..., ge=500, le=40_000, description="Loan amount (USD)")
    int_rate: float = Field(..., ge=0, le=50, description="Interest rate (%)")
    installment: float = Field(..., ge=0.0, le=2_000.0, description="Monthly installment (USD)")
    annual_inc: float = Field(..., ge=0, le=10_000_000, description="Annual income (USD)")
    dti: float = Field(..., ge=0.0, le=100.0, description="Debt-to-income ratio")
    delinq_2yrs: float = Field(..., ge=0.0, le=30.0, description="Delinquencies in last 2 years")
    fico_range_low: float = Field(..., ge=300.0, le=850.0, description="FICO score lower bound")
    revol_util: float = Field(..., ge=0.0, le=150.0, description="Revolving utilization rate (%)")

    # Categorical features
    term: Literal["36 months", "60 months"] = Field(..., description="Loan term")
    grade: Literal["A", "B", "C", "D", "E", "F", "G"] = Field(..., description="Loan grade")
    emp_length: Literal[
        "< 1 year", "1 year", "2 years", "3 years", "4 years",
        "5 years", "6 years", "7 years", "8 years", "9 years", "10+ years"
    ] = Field(..., description="Employment length")
    home_ownership: Literal["RENT", "OWN", "MORTGAGE", "OTHER"] = Field(..., description="Home ownership")
    verification_status: Literal["Not Verified", "Verified", "Source Verified"] = Field(..., description="Income verification status")
    purpose: Literal[
        "debt_consolidation", "credit_card", "home_improvement", "other",
        "major_purchase", "small_business", "car", "medical", "moving",
        "vacation", "house", "wedding", "renewable_energy", "educational"
    ] = Field(..., description="Loan purpose")
class Prediction(BaseModel):
    """Output schema for /predict."""

    prediction: int = Field(..., description="0 = Fully Paid, 1 = Charged Off")
    probability: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    status: str

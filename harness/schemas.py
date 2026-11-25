from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Decision(str, Enum):
    APPROVE = "approve"
    REAUTH = "reauth"
    BLOCK = "block"


class Mandate(BaseModel):
    """What the user authorized the agent to do."""
    user_id: str
    max_per_purchase: float
    total_budget: float
    allowed_categories: list[str]
    expires_at: datetime


class PurchaseRequest(BaseModel):
    """What the agent sends to the harness."""
    request_id: str
    user_id: str
    user_query: str          # what the user originally asked the agent to find
    item: str
    category: str
    merchant: str
    price: float = Field(gt=0)

    # Optional order details used by anomaly checks.
    quantity: int = Field(default=1, ge=1)
    perishable: bool = Field(default=False)

    timestamp: datetime
    mandate: Mandate


class Signal(BaseModel):
    """One check's result, e.g. 'duplicate purchase in 15 days'."""
    name: str
    triggered: bool
    weight: float
    detail: str


class DecisionResponse(BaseModel):
    """What the harness sends back."""
    request_id: str
    decision: Decision
    reason: str
    signals: list[Signal]
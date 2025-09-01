from pydantic import BaseModel
from typing import Union
from datetime import datetime

class Transaction(BaseModel):
    transaction_id: int
    merchant_id: int
    user_id: int
    card_number: str
    transaction_date: datetime
    transaction_amount: float
    device_id: Union[str, int, None] = None
    has_cbk: bool = False

class RecommendationResponse(BaseModel):
    transaction_id: int
    recommendation: str  # "APPROVE" or "DENY"
from fastapi import APIRouter
from src.models import Transaction, RecommendationResponse
from src.services import CheckFraudService

router = APIRouter()

service = CheckFraudService()

@router.post("/transaction", response_model=RecommendationResponse)
async def predict(transaction: Transaction):
    result = await service.execute(transaction)
    return RecommendationResponse(transaction_id=result[0], recommendation=result[1])
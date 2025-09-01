from pathlib import Path
from typing import Any
import joblib
import pandas as pd
from src.models import Transaction
from src.utils import process_pipeline

BASE_PATH = Path(__file__).parent

class CheckFraudService:
    async def _model_and_preprocessor(self) -> tuple[Any, Any]:
        model = joblib.load(f"{BASE_PATH}/model_ml/anti_fraud_model.pkl")
        preprocessor = joblib.load(f"{BASE_PATH}/model_ml/preprocessor.pkl")
        return model, preprocessor

    async def execute(self, transaction: Transaction) -> tuple[str, float]:
        model, preprocessor = await self._model_and_preprocessor()

        transaction_dict = transaction.model_dump()
        
        df_transaction = pd.DataFrame([transaction_dict])

        transaction_id = df_transaction['transaction_id'].values

        df_proc = process_pipeline(df_transaction).drop(columns=['is_fraud'], errors='ignore')
        df_proc = df_proc.fillna(0)
    
        df_proc_transformed = preprocessor.transform(df_proc.drop(columns=['user_id', 'transaction_id'], errors='ignore'))
  
        prediction = model.predict(df_proc_transformed)[0]
        proba = model.predict_proba(df_proc_transformed)[0][prediction]
   
        result = "deny" if prediction == 1 else "approve"

        return transaction_id, result, proba
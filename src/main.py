from fastapi import FastAPI
from src.controllers import router

app = FastAPI(
    title="Anti Fraud API",
    description="API for real-time fraud detection using machine learning models",
)
app.include_router(router)
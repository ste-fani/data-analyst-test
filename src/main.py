from fastapi import FastAPI
from src.controllers import router

app = FastAPI(
    title="Anti Fraud API",
    description="Random Description",
)
app.include_router(router)
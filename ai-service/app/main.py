import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .model_service import ModelUnavailableError, fraud_model
from .schemas import HealthResponse, PredictionRequest, PredictionResponse
from .settings import settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    fraud_model.load()
    yield


app = FastAPI(
    title="Real-Time Fraud Detection API",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model_loaded=fraud_model.loaded,
        model_version=settings.model_id,
    )


@app.get("/ready", response_model=HealthResponse)
def ready() -> HealthResponse:
    if not fraud_model.loaded:
        fraud_model.load()
    if not fraud_model.loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction model is not ready",
        )
    return HealthResponse(
        status="ready",
        model_loaded=True,
        model_version=settings.model_id,
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        return PredictionResponse(**fraud_model.predict(request.text))
    except ModelUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction model is unavailable",
        ) from exc

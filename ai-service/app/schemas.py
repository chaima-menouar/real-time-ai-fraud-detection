from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class PredictionRequest(BaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=2000)]


class PredictionResponse(BaseModel):
    category: str
    risk: bool
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str

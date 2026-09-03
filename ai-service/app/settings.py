import os
from dataclasses import dataclass


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    model_path: str = os.getenv("MODEL_PATH", "/models/xlm_roberta_fraud_classifier")
    model_id: str = os.getenv("MODEL_ID", "xlm-roberta-fraud-classifier")
    allow_remote_model: bool = _as_bool(os.getenv("ALLOW_REMOTE_MODEL", "false"))
    max_length: int = int(os.getenv("MAX_LENGTH", "256"))
    cors_origins: tuple[str, ...] = tuple(
        item.strip()
        for item in os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")
        if item.strip()
    )


settings = Settings()

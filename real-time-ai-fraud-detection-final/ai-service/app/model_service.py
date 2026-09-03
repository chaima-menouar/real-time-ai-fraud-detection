import json
import logging
from pathlib import Path
from threading import Lock

from .labels import is_risk_label, normalize_label
from .settings import settings

LOGGER = logging.getLogger(__name__)


class ModelUnavailableError(RuntimeError):
    pass


class FraudModel:
    """Lazily loads a local Hugging Face sequence-classification model."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._tokenizer = None
        self._model = None
        self._torch = None
        self._id_to_label: dict[int, str] = {}
        self._load_error: str | None = None

    @property
    def loaded(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    @property
    def load_error(self) -> str | None:
        return self._load_error

    def load(self) -> None:
        if self.loaded:
            return
        with self._lock:
            if self.loaded:
                return
            source = Path(settings.model_path)
            has_weights = source.exists() and any(
                (source / name).exists()
                for name in ("model.safetensors", "pytorch_model.bin")
            )
            if not has_weights and not settings.allow_remote_model:
                self._load_error = (
                    f"No model weights found in {source}. "
                    "Train/export the model or explicitly enable a trusted remote model."
                )
                LOGGER.warning(self._load_error)
                return

            model_source = str(source if has_weights else settings.model_id)
            try:
                import torch
                from transformers import AutoModelForSequenceClassification, AutoTokenizer

                tokenizer = AutoTokenizer.from_pretrained(
                    model_source, local_files_only=has_weights
                )
                model = AutoModelForSequenceClassification.from_pretrained(
                    model_source, local_files_only=has_weights
                )
                model.eval()
                id_to_label = self._read_labels(source) or {
                    int(key): str(value) for key, value in model.config.id2label.items()
                }
                generic = all(label.upper().startswith("LABEL_") for label in id_to_label.values())
                if generic or not any(not is_risk_label(label) for label in id_to_label.values()):
                    raise ValueError(
                        "A real label mapping containing a normal class is required"
                    )
                self._torch = torch
                self._tokenizer = tokenizer
                self._model = model
                self._id_to_label = id_to_label
                self._load_error = None
                LOGGER.info("Model loaded from configured source")
            except Exception as exc:  # startup must remain observable through /ready
                self._torch = None
                self._tokenizer = None
                self._model = None
                self._id_to_label = {}
                self._load_error = f"Unable to load model: {type(exc).__name__}"
                LOGGER.exception("Model loading failed")

    @staticmethod
    def _read_labels(source: Path) -> dict[int, str]:
        mapping_file = source / "label_mapping.json"
        if mapping_file.exists():
            data = json.loads(mapping_file.read_text(encoding="utf-8"))
            return {int(key): str(value) for key, value in data.items()}
        return {}

    def predict(self, text: str) -> dict[str, object]:
        self.load()
        if not self.loaded:
            raise ModelUnavailableError(self._load_error or "Model is unavailable")

        inputs = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=settings.max_length,
        )
        with self._torch.inference_mode():
            logits = self._model(**inputs).logits[0]
            probabilities = self._torch.softmax(logits, dim=-1)
            class_id = int(self._torch.argmax(probabilities).item())
            confidence = float(probabilities[class_id].item())

        raw_label = self._id_to_label.get(
            class_id,
            str(self._model.config.id2label.get(class_id, f"class_{class_id}")),
        )
        category = normalize_label(raw_label)
        return {
            "category": category,
            "risk": is_risk_label(category),
            "confidence": confidence,
            "model_version": settings.model_id,
        }


fraud_model = FraudModel()

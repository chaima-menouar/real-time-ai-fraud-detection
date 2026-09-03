# Architecture

The browser sends live and comment operations to Spring Boot. Spring persists domain data, asks FastAPI for a model prediction, then broadcasts the saved comment to subscribed browsers. FastAPI owns model loading and inference only.

## Prediction contract

Request:

```json
{ "text": "comment to classify" }
```

Response:

```json
{
  "category": "normal",
  "risk": false,
  "confidence": 0.94,
  "model_version": "xlm-roberta-fraud-classifier"
}
```

Spring returns `503 Service Unavailable` when the model cannot produce a real prediction. There is no keyword or random fallback.

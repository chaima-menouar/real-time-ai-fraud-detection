# Deployment notes

## Local demo

1. Export a trained Hugging Face model to `ml/models/xlm_roberta_fraud_classifier/`.
2. Copy `.env.example` to `.env` and adjust values if needed.
3. Run `docker compose up --build`.

## AWS reference deployment

- store the model artifact in a private, encrypted S3 bucket;
- run FastAPI and Spring containers in ECS/Fargate or App Runner;
- store runtime secrets in Secrets Manager, not source control;
- put both services behind HTTPS and restrict the AI service to the backend network;
- use RDS PostgreSQL instead of H2;
- send application metrics to CloudWatch without logging raw comments;
- configure autoscaling, budgets, health checks, and least-privilege IAM roles.

The repository intentionally contains no AWS credentials or account-specific identifiers.

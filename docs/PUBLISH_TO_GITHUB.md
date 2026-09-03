# Publish this clean edition

Use a new empty GitHub repository named `real-time-ai-fraud-detection`. Do not initialize it with a README, license, or `.gitignore` because those files already exist here.

From PowerShell inside the extracted folder:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "feat: publish cleaned real-time fraud detection system"
git remote add origin https://github.com/chaima-menouar/real-time-ai-fraud-detection.git
git push -u origin main
```

Before `git commit`, confirm that `git status` does **not** list raw datasets, `.env`, `test_predictions.csv`, checkpoints, or model weight files.

Recommended repository description:

> Human-reviewed multilingual fraud detection for e-learning using XLM-RoBERTa, FastAPI, Spring Boot, WebSocket, Docker, and an AWS deployment design.

Recommended topics:

`machine-learning`, `nlp`, `xlm-roberta`, `fastapi`, `spring-boot`, `websocket`, `docker`, `aws`, `responsible-ai`

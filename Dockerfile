FROM python:3.12-slim
WORKDIR /app
COPY dedup.py sample_alerts.csv ./
CMD ["python", "dedup.py", "sample_alerts.csv", "clean_alerts.csv"]
# Alert Deduplicator

Removes duplicate news alerts and merges their topics. Two alerts count as the same story if they have the same URL or title (ignoring caps, punctuation, `www.`, and tracking params).

Built to learn CI/CD with GitHub Actions and Docker.

## Run
```bash
python dedup.py sample_alerts.csv clean_alerts.csv
```

## Test
```bash
pip install -r requirements.txt
pytest -v
```

## Docker
```bash
docker build -t alert-dedup .
docker run --rm alert-dedup
```
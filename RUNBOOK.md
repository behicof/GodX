# Runbook

## Local Development

1. Install dependencies (e.g. `pip install -r requirements.txt` if present).
2. Run tests with `make test`.
3. Use `docker-compose` from `deploy/` to spin up Redis, PostgreSQL, ClickHouse, Prometheus, and Grafana.

## Deployment

- Ensure environment variables for API keys are set (.env).
- `docker-compose up -d` will start Redis, PostgreSQL, ClickHouse, Prometheus and Grafana.
- Logs are JSON formatted via structlog and can be scraped by Prometheus.

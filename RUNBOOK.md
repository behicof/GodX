# Runbook

## Local Development

1. Install dependencies (e.g. `pip install -r requirements.txt` if present).
2. Run tests with `make test`.
3. Use `docker-compose` from `deploy/` to spin up infra services.

### Supply Chain Helpers

- Offline mode: `OFFLINE=1 make vendor`
- Quick restore: `make vendor-clean && make vendor`
- Update flow: `make shas` → submit PR with updated `repos.lock`

## Deployment

- Ensure environment variables for API keys are set (.env).
- `docker-compose up -d` will start app, Redis, PostgreSQL, Prometheus and Grafana.
- Logs are JSON formatted via structlog and can be scraped by Prometheus.

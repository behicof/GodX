# Omni-Arb

Omni-Arb is a lightweight skeleton for a deterministic arbitrage and directional
trading research platform. It demonstrates an end-to-end flow from opportunity
intake through risk checks, execution and logging.

## Layout

- `core/` – trading primitives
- `orchestrator/` – pipeline wiring modules together
- `nlp/` – placeholders for FinGPT/FinRAG integrations
- `research/` – backtesting utilities
- `deploy/` – docker-compose and infra helpers
- `config/` – configuration files
- `tests/` – pytest test suite
## Infrastructure

After bringing up services with `docker-compose up -d` (see `RUNBOOK.md`), you can verify Prometheus and the app are healthy:

```bash
curl -s http://localhost:9090/-/healthy
curl -s http://localhost:3000/login
```

## Getting Started

```bash
make test
```

## Metrics Smoke Test

Run a tiny exporter that emits dummy Prometheus metrics:

```bash
make metrics-smoke PORT=8000
curl -s http://localhost:8000/metrics
```

The `PORT` variable is optional and defaults to `8000`.

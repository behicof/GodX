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

### Metrics configuration

Metrics behaviour is driven by a few environment variables:

- `METRICS_MODE` – one of `auto`, `push`, `export` or `log` (defaults to `auto`).
- `PUSHGW_URL` – URL of a Prometheus Pushgateway for `push` mode.
- `METRICS_PORT` – port for the HTTP exporter when using `export` mode (defaults to `8000`).

## Getting Started

```bash
make test
```

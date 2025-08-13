# Omni-Arb

Omni-Arb is a minimal end-to-end scaffold for a multi-strategy trading platform.
It includes core execution/risk components, an orchestrator loop, NLP hooks and
research stubs. The project targets Python 3.10+, Redis/PostgreSQL storage and
Prometheus/Grafana monitoring.

## Layout

- `core/` – execution strategies, exchange connectors, risk utilities and data layer
- `orchestrator/` – FinRobot-style flow
- `nlp/` – FinGPT/FinRAG hooks
- `research/` – training and backtesting helpers
- `deploy/` – docker-compose, Prometheus and Grafana assets
- `config/` – YAML configuration templates and `.env.example`
- `tests/` – pytest suite

## Usage

```bash
make test            # run tests
make up              # start infra (redis, postgres, prometheus, grafana)
make orchestrator    # run one orchestrator cycle
```

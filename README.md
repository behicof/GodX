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

## Metrics

Prometheus-style metrics are available via helpers in `libs/metrics.py`. Metrics
can be exported over HTTP or pushed to a Pushgateway.

```python
from libs.metrics import init_metrics, push_metrics

# Start an HTTP server on port 8000
init_metrics(port=8000)

# Push collected metrics to a gateway
push_metrics(job="godx", gateway="localhost:9091")
```

The executor and risk manager automatically publish latency and error counters
(`executor_execute_latency_seconds`, `executor_execute_errors_total`,
`risk_manager_check_latency_seconds`, `risk_manager_check_errors_total`).

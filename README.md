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

## Basis Backtest

`research.simulate_basis` runs a simple basis-trading backtest.

### Input Data

Provide spot and futures prices as CSV or Parquet with columns:

```csv
timestamp,spot,future
2024-01-01T00:00:00Z,100,105
2024-01-01T00:01:00Z,101,104
```

### Usage

```python
import pandas as pd
from research import BTConfig, simulate_basis

df = pd.read_csv("prices.csv")
cfg = BTConfig(fee=0.001, slippage=0.0005, latency=1, long_entry=0.02, short_entry=0.02)
result = simulate_basis(df, cfg)
print(result)
```

Assumptions:

- One unit notional per leg.
- Fees and slippage applied to each open/close leg.
- Trades enter when the basis exceeds thresholds and exit when it crosses zero.

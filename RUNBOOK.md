# Runbook

1. `cp config/.env.example config/.env` and fill in keys.
2. Edit `config/exchanges.yml`, `config/thresholds.yml`, `config/risk.yml` and `config/symbols.yml`.
3. `make up` to start Redis, PostgreSQL, Prometheus and Grafana.
4. `make logger` to launch the logging service.
5. `make orchestrator` for one trading cycle.
6. `make backtest` to run threshold analysis.
7. `make train-ppo` to train a DRL agent stub.
8. View Grafana at `http://localhost:3000`.

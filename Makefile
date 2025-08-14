# ===== Vars =====
PY := python3
PIP := pip
DC := docker compose
APP := omni-arb

# ===== Default =====
.PHONY: help
help:
	@echo "Targets: setup | up | down | logs | logger | orchestrator | backtest | metrics-smoke | train-ppo | test"

# ===== Setup (py + docker) =====
.PHONY: setup
setup: .venv req dockercheck
	@echo "[OK] setup done."

.venv:
	$(PY) -m venv .venv && . .venv/bin/activate && $(PIP) install -U pip

.PHONY: req
req:
	. .venv/bin/activate && $(PIP) install -r requirements.txt || true

.PHONY: dockercheck
dockercheck:
	@command -v docker >/dev/null || (echo "Install Docker first."; exit 1)

# ===== Compose =====
.PHONY: up
up:
	$(DC) -f deploy/docker-compose.yml up -d

.PHONY: down
down:
	$(DC) -f deploy/docker-compose.yml down -v

.PHONY: logs
logs:
	$(DC) -f deploy/docker-compose.yml logs -f --tail=200

# ===== App Entrypoints (dummy) =====
.PHONY: logger
logger:
	$(PY) -m apps.ingest.logger_metrics

.PHONY: orchestrator
orchestrator:
	$(PY) -m orchestrator.metrics_hook

.PHONY: backtest
backtest:
	$(PY) -m apps.backtester.metrics

.PHONY: metrics-smoke
metrics-smoke: logger orchestrator backtest

.PHONY: train-ppo
train-ppo:
	. .venv/bin/activate && $(PY) apps/research/train_ppo.py --symbol BTCUSDT --epochs 10

.PHONY: test
test:
	$(PY) -m pytest -q

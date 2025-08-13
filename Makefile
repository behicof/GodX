# ===== Vars =====
PY := python3
PIP := pip
DC := docker compose
APP := omni-arb

# ===== Default =====
.PHONY: help
help:
	@echo "Targets: setup | up | down | logs | logger | orchestrator | backtest | train-ppo | test"

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
	. .venv/bin/activate && $(PY) apps/ingest/logger.py

.PHONY: orchestrator
orchestrator:
	. .venv/bin/activate && $(PY) apps/executor/orchestrator.py

.PHONY: backtest
backtest:
	. .venv/bin/activate && $(PY) apps/backtester/run_backtest.py

.PHONY: train-ppo
train-ppo:
	. .venv/bin/activate && $(PY) apps/research/train_ppo.py --symbol BTCUSDT --epochs 10

.PHONY: test
test:
	. .venv/bin/activate && pytest -q

.PHONY: shas vendor vendor-clean
shas:	# refresh repos.lock (uses scripts/fetch_shas.sh)
	./scripts/fetch_shas.sh

vendor:	# clone & pin from repos.lock
	./scripts/clone_and_pin.sh

vendor-clean:
	rm -rf vendor

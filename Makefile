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

# ===== Supply chain =====
.PHONY: shas vendor verify-vendor sbom license-scan smoke

shas:
        ./scripts/fetch_shas.sh

vendor:
        ./scripts/clone_and_pin.sh repos.lock

verify-vendor:
        . .venv/bin/activate && $(PY) scripts/verify_vendor.py repos.lock vendor

sbom:
        @command -v cdxgen >/dev/null || (echo "cdxgen not installed" && exit 1)
        cdxgen -r . -o sbom.json

license-scan:
        @command -v pip-licenses >/dev/null || (echo "pip-licenses not installed" && exit 1)
        pip-licenses --format=json --output-file=licenses.json

smoke:
        . .venv/bin/activate && $(PY) scripts/smoke.py

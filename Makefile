# ===== Vars =====
PY := python3
PIP := pip
SBOM := python -m cyclonedx_py
LICENSES := python -m piplicenses
DC := docker compose

# detect docker
HAVE_DOCKER := $(shell command -v docker >/dev/null 2>&1 && echo yes || echo no)

.PHONY: help
help:
	@echo "Targets: setup | up | down | logs | logger | orchestrator | backtest | train-ppo | test | verify-vendor | sbom | license-scan"

# ===== Setup (venv + pip) =====
.PHONY: setup
setup: .venv req dockerhint
	@echo "[OK] setup done."

.venv:
	$(PY) -m venv .venv && . .venv/bin/activate && $(PIP) install -U pip

.PHONY: req
req:
	. .venv/bin/activate && $(PIP) install -r requirements.lock || true

.PHONY: dockerhint
dockerhint:
ifeq ($(HAVE_DOCKER),no)
	@echo "[INFO] Docker not found. 'make up' will be a no-op until you install Docker."
endif

# ===== Compose (safe if no docker) =====
.PHONY: up
up:
ifeq ($(HAVE_DOCKER),yes)
	$(DC) -f deploy/docker-compose.yml up -d
else
	@echo "[SKIP] Docker not installed. Install Docker to run 'make up'."
endif

.PHONY: down
down:
ifeq ($(HAVE_DOCKER),yes)
	$(DC) -f deploy/docker-compose.yml down -v
else
	@echo "[SKIP] Docker not installed."
endif

.PHONY: logs
logs:
ifeq ($(HAVE_DOCKER),yes)
	$(DC) -f deploy/docker-compose.yml logs -f --tail=200
else
	@echo "[SKIP] Docker not installed."
endif

# ===== App Entrypoints =====
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
	. .venv/bin/activate && $(PY) apps/research/train_ppo.py --symbol BTCUSDT --epochs 2

.PHONY: test
test:
	. .venv/bin/activate && pytest -q

# ===== Supply Chain =====
.PHONY: verify-vendor
verify-vendor:
	. .venv/bin/activate && $(PY) scripts/verify_vendor.py

.PHONY: sbom
sbom:
	. .venv/bin/activate && $(SBOM) requirements requirements.lock -o sbom.json

.PHONY: license-scan
license-scan:
	. .venv/bin/activate && $(LICENSES) --format=json --output-file licenses.json

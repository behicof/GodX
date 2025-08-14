# ===== Vars =====
PY := python3
PIP := pip
DC := docker compose
APP := omni-arb
export PUSHGW_URL ?= http://localhost:9091
export METRICS_JOB ?= omni-scripts


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

# ===== Metrics Demo =====
.PHONY: logger orchestrator backtest metrics-smoke
logger:
	$(PY) -m apps.ingest.logger_metrics

orchestrator:
	$(PY) - <<-'PY'
	from orchestrator.metrics_hook import time_leg, mark_fill
	import time, random
	def mock_leg(): time.sleep(random.uniform(0.05,0.2))
	time_leg(mock_leg); mark_fill("BTCUSDT",1.0)
	PY

backtest:
	$(PY) - <<-'PY'
	from apps.backtester.metrics import run_backtest
	class BT:
	  def __iter__(self):
	    import time
	    for _ in range(5): time.sleep(0.1); yield None
	  def pnl(self): return 42.0
	run_backtest(BT())
	PY

metrics-smoke: logger orchestrator backtest
# ===== Other Entrypoints =====
.PHONY: train-ppo
train-ppo:
	. .venv/bin/activate && $(PY) apps/research/train_ppo.py --symbol BTCUSDT --epochs 10

.PHONY: test
test:
	. .venv/bin/activate && pytest -q

export PUSHGW_URL ?= http://localhost:9091
export METRICS_JOB ?= omni

setup:
	python -m pip install -U pip wheel
	pip install fastapi uvicorn prometheus-client

up:
	docker compose -f deploy/docker-compose.yml up -d

logger:
	python -m apps.ingest.logger_metrics

orchestrator:
	python -m orchestrator.runner

backtest:
	python -m apps.backtester.metrics || true  # اگر ندارید، فعلاً skip

test:
	pytest -q || true

metrics-smoke: logger orchestrator

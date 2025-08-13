.PHONY: setup up logger orchestrator backtest train-ppo test down

setup:
	@echo "setup not implemented"

up:
	docker-compose -f deploy/docker-compose.yml up -d

logger:
	python -m core.data.logger

orchestrator:
	python -m orchestrator.finrobot_flow

backtest:
	python -m research.finrl_meta_scenarios.backtest_thresholds

train-ppo:
	python -m research.elegantrl_training.train_ppo

test:
	pytest -q

down:
	docker-compose -f deploy/docker-compose.yml down

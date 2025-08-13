.PHONY: test format

test:
	pytest -q

format:
	black .

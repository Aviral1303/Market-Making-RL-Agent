PYTHON=python3
PIP=pip3
VENV=.venv

.PHONY: venv install test lint format type backtest grid train evaluate api-up api-down mlflow-up mlflow-down stack-up stack-down db-init api-health package

venv:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install --upgrade pip

install:
	$(PIP) install -r requirements.txt

 test:
	pytest -q

lint:
	ruff check .

format:
	ruff check --fix . && black .

type:
	mypy .

backtest:
	mmrl backtest

grid:
	mmrl grid

train:
	mmrl train

evaluate:
	mmrl evaluate

api-up:
	docker compose up -d api redis worker

api-down:
	docker compose down api worker redis

mlflow-up:
	docker compose up -d mlflow

mlflow-down:
	docker compose stop mlflow

stack-up:
	docker compose up -d redis worker api mlflow

stack-down:
	docker compose down

db-init:
	$(PYTHON) -c "from storage.duckdb import init_db; init_db(); print('ok')"

api-health:
	curl -s http://localhost:8000/health

package:
	python3 -m build
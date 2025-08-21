# HTTP API

Start services:
```
docker compose up -d redis worker api mlflow
```

## Endpoints
- Health: `GET /health`
- Backtest: `POST /backtest` body: `{ "steps": 1000 }`
- Grid: `POST /grid`
- Train: `POST /train`
- Evaluate: `POST /evaluate`
- Evaluate Multi: `POST /evaluate_multi` (sync=false by default)
- Jobs: `GET /jobs`, `GET /jobs/{id}`
- Runs: `GET /runs?limit=&offset=`, `GET /runs/{run}`, `GET /runs/{run}/artifacts`, `GET /runs/{run}/download`
- Trades: `GET /trades/{run_id}`
- Metrics: `GET /metrics/{run_id}`
- Config schema: `GET /config/schema`

## Examples
```
curl -X POST http://localhost:8000/backtest -H 'Content-Type: application/json' -d '{"steps": 500}'
curl http://localhost:8000/runs?limit=10
curl -L -o run.zip http://localhost:8000/runs/<run_dir>/download
```
# Workflows

## Prototype
1. `mmrl backtest`
2. `mmrl report results/<run>`

## Compare agents
1. `mmrl evaluate`
2. Inspect MLflow UI or saved comparison plots

## Hyperparameter search
- Grid:
```
mmrl grid
```
- Optuna:
```
python3 experiments/hyperopt.py
```

## Data-backed test
1. Fetch Parquet with CCXT
2. Replay with `MarketReplay` and evaluate

## API orchestration
1. `docker compose up -d redis worker api mlflow`
2. Submit jobs via HTTP and monitor `/jobs`
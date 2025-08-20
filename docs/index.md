---
title: MMRL Documentation
---

# Market Making RL (MMRL)

Welcome to the MMRL docs. This site covers:

- Quickstart and install
- Architecture and components
- CLI and API usage
- Experiments and analysis
- Configuration schema

## Quickstart

```
pip install -r requirements.txt
mmrl backtest
mmrl evaluate
```

## CLI

```
mmrl --help
mmrl config-validate
mmrl config-schema
mmrl fetch-data --exchange binance --symbol BTC/USDT --limit 1000 --out data/btc.parquet
```

## API

```
docker compose up -d redis worker api mlflow
curl http://localhost:8000/health
curl http://localhost:8000/config/schema
```

See also: performance_metrics.md


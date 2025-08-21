# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-08-20
- Initial public-ready release candidate
- CLI: backtest, grid, train, evaluate, analyze, fetch-data, config-validate, config-schema
- API: backtest, grid, train, evaluate, evaluate_multi, jobs, runs (pagination), artifacts listing & zip download, config schema, trades/metrics fetch, Prometheus metrics
- Environments: single-asset LOB with OU/regimes; multi-asset (correlated) env; Gym wrappers
- Agents: Naive, Inventory-aware, Avellaneda–Stoikov, Depth-aware, Mean-Reversion, Momentum; PPO baseline
- Persistence: DuckDB for runs/metrics/trades; MLflow logging; reproducibility stamps (git hash, config hash, pip freeze)
- Analysis: heatmaps, multi-asset plots, metrics utilities
- Docs: MkDocs scaffold, performance metrics guide; Colab notebooks added
- Docker/Compose stack for API+MLflow+Redis/RQ

## [0.1.2] - 2025-08-20
- Programmatic API: `mmrl.run_backtest(config)` and `__version__`
- CLI: `report` command stabilized; `fetch-data` adds `--since` and `--max-pages`
- CCXT loader: pagination/retries and `since` support
- Demo: improved README GIF generated from real CLI output; curated positive benchmarks
# CLI

## Commands
- `mmrl backtest [--config path]`
- `mmrl evaluate [--config path]`
- `mmrl grid [--config path]`
- `mmrl analyze <returns.csv> [--plot] [--output-file out.csv]`
- `mmrl report <run_dir|csv> [--out report.html]`
- `mmrl fetch-data --exchange binance --symbol BTC/USDT --limit 1000 --out data/btc.parquet [--since ts_ms] [--max-pages N]`
- `mmrl config-validate`
- `mmrl config-schema`

## Tips
- If `configs/inventory.yaml` does not exist, `mmrl backtest` auto-generates a default config.
- Use `mmrl report` to produce a single HTML you can share.
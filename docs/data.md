# Data

## CCXT Fetch
Fetch exchange trades to Parquet:
```
mmrl fetch-data --exchange binance --symbol BTC/USDT --limit 1000 --out data/btc.parquet --since 1700000000000 --max-pages 20
```

## Replay
Use `adapters/market_replay.py` and `examples/replay_quickstart.py` to iterate through recorded data and map to env-compatible ticks.

## Pluggable data adapters
Provide your own data source by implementing a minimal adapter and loading it dynamically.

### Base interface
```python
from mmrl.data.base import DataAdapter

class MyAdapter(DataAdapter):
    def iter_ticks(self):
        # yield dicts with keys your env expects (e.g. time, mid_price, best_bid, best_ask, volume)
        yield {"time": 1, "mid_price": 100.0}
```

### Dynamic loading
```python
from mmrl.data import load_adapter
adapter = load_adapter('mmrl.data.csv_adapter:CSVAdapter', path='data/file.csv', mapping={'mid_price': 'mid'})
for tick in adapter.iter_ticks():
    pass
```

### Streaming into the env
You can feed ticks into the env to progress reference state:
```python
from env.simple_lob_env import SimpleLOBEnv
from mmrl.data import load_adapter

env = SimpleLOBEnv()
adapter = load_adapter('mmrl.data.csv_adapter:CSVAdapter', path='data/file.csv', mapping={'mid_price': 'mid'})
for tick in adapter.iter_ticks():
    state = env.step_from_tick(tick)
```

## Storage
- DuckDB stores `runs`, `metrics`, `trades` for local analysis.
- Artifacts (CSV/plots/metrics.json) in `results/<timestamp_tag>/`.
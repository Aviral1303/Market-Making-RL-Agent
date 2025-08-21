# Extending

## Add a new agent
Create a class with a `quote(mid_price: float, inventory: int) -> (bid, ask)` method and wire it into `experiments/evaluate_agents.py`.

## Customize microstructure
Edit `env/simple_lob_env.py` (fills, fees, slippage, OU/regimes). For multi-asset/regime-conditioned depth, see `env/multi_asset_env.py`.

## Programmatic hooks
Use `mmrl.run_backtest(config)` in your own scripts. Persist your own artifacts to the run directory.
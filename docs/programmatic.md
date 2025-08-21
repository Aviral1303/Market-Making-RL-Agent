# Programmatic API

Use MMRL from Python code for scripting and integration.

## Backtest
```python
from mmrl import run_backtest
cfg = {"run_tag": "scripted", "seed": 7, "steps": 1000, "output_dir": "results",
        "agent": {"spread": 0.1, "inventory_sensitivity": 0.05},
        "market": {"ou_enabled": True, "ou": {"mu": 100, "kappa": 0.05, "sigma": 0.5, "dt": 1.0},
                    "vol_regime": {"enabled": True, "high_sigma_scale": 3.0, "switch_prob": 0.02}},
        "execution": {"base_arrival_rate": 1.0, "alpha": 1.5},
        "fees": {"fee_bps": 1.0, "slippage_bps": 2.0, "maker_bps": -0.5, "taker_bps": 1.0}}
run_dir, metrics = run_backtest(cfg)
print(run_dir, metrics)
```
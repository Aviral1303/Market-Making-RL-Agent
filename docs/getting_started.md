# Getting Started

## Install
- Backtest + storage:
```
pip install "mmrl[api]"
```
- RL extras (PPO, Gym/SB3):
```
pip install "mmrl[api]" "mmrl[rl]"
```

## Quickstart (CLI)
```
mmrl backtest
mmrl report results/<latest_run_dir> --out report.html
```

## Quickstart (Python)
```python
from mmrl import run_backtest
cfg = {"run_tag": "demo", "seed": 42, "steps": 500, "output_dir": "results",
        "agent": {"spread": 0.1, "inventory_sensitivity": 0.05},
        "market": {"ou_enabled": True, "ou": {"mu": 100, "kappa": 0.05, "sigma": 0.5, "dt": 1.0},
                    "vol_regime": {"enabled": True, "high_sigma_scale": 3.0, "switch_prob": 0.02}},
        "execution": {"base_arrival_rate": 1.0, "alpha": 1.5},
        "fees": {"fee_bps": 1.0, "slippage_bps": 2.0, "maker_bps": -0.5, "taker_bps": 1.0}}
run_dir, metrics = run_backtest(cfg)
print(run_dir, metrics)
```
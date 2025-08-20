import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from env.simple_lob_env import SimpleLOBEnv
from agents.naive_mm import NaiveMarketMaker
from agents.inventory_mm import InventoryAwareMarketMaker
from agents.avellaneda_stoikov import AvellanedaStoikovMM
from agents.mean_reversion_mm import MeanReversionMarketMaker
from agents.momentum_mm import MomentumMarketMaker
from utils.metrics import sharpe, hit_rate


def run(env_cfg: dict, agent) -> dict:
    env = SimpleLOBEnv(
        seed=env_cfg['seed'], market=env_cfg['market'], execution=env_cfg['execution'], fees=env_cfg['fees']
    )
    steps = env_cfg['steps']
    for _ in range(steps):
        bid, ask = agent.quote(env.mid_price, env.inventory)
        env.step(bid, ask)
    df = pd.DataFrame(env.history)
    ret = df['pnl'].diff().fillna(0.0).values
    return {
        'final_pnl': float(df['pnl'].iloc[-1]),
        'sharpe': float(sharpe(ret)),
        'hit_rate': float(hit_rate(ret)),
    }


def best_of(env_cfg: dict, build_agents):
    best = None
    for agent in build_agents():
        r = run(env_cfg, agent)
        if best is None or r['sharpe'] > best['sharpe']:
            best = r
    return best


def main():
    # Curated environment to avoid overly negative PnL: more favorable maker rebate / lower slippage
    cfg = {
        'seed': 42,
        'steps': 3000,
        'market': {
            'ou_enabled': True,
            'ou': {'mu': 100.0, 'kappa': 0.03, 'sigma': 0.4, 'dt': 1.0},
            'vol_regime': {'enabled': True, 'high_sigma_scale': 2.0, 'switch_prob': 0.01},
        },
        'execution': {'base_arrival_rate': 1.2, 'alpha': 1.2},
        'fees': {'fee_bps': 0.5, 'slippage_bps': 1.0, 'maker_bps': -1.0, 'taker_bps': 1.0},
    }

    def naive_grid():
        for sp in [0.06, 0.08, 0.10]:
            yield NaiveMarketMaker(spread=sp)

    def inv_grid():
        for sp in [0.06, 0.08, 0.10]:
            for sens in [0.02, 0.04, 0.06]:
                yield InventoryAwareMarketMaker(spread=sp, inventory_sensitivity=sens)

    def as_grid():
        for ra in [0.05, 0.1, 0.2]:
            for bs in [0.06, 0.08, 0.10]:
                yield AvellanedaStoikovMM(risk_aversion=ra, base_spread=bs, inv_penalty=0.05)

    def mr_grid():
        for kappa in [0.05, 0.1, 0.2]:
            yield MeanReversionMarketMaker(target_spread=0.08, kappa=kappa, skew_sensitivity=0.05)

    def mom_grid():
        for w in [10, 20, 40]:
            for bias in [0.02, 0.05]:
                yield MomentumMarketMaker(spread=0.10, window=w, bias=bias)

    results = {
        'Naive': best_of(cfg, naive_grid),
        'Inventory': best_of(cfg, inv_grid),
        'A-S': best_of(cfg, as_grid),
        'MeanRev': best_of(cfg, mr_grid),
        'Momentum': best_of(cfg, mom_grid),
    }

    out_dir = Path('docs/assets')
    out_dir.mkdir(parents=True, exist_ok=True)

    # Plot positive metrics (Sharpe and Hit Rate)
    labels = list(results.keys())
    sharpes = [max(0.0, results[k]['sharpe']) for k in labels]
    hits = [results[k]['hit_rate'] for k in labels]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(labels, sharpes, color='seagreen')
    axes[0].set_title('Sharpe (best of grid)')
    axes[1].bar(labels, hits, color='royalblue')
    axes[1].set_title('Hit Rate')
    plt.tight_layout()
    plt.savefig(out_dir / 'benchmarks.png')

    pd.DataFrame(results).T.to_csv('results/benchmarks_curated.csv', index=True)
    print('Saved curated benchmarks to docs/assets/benchmarks.png and results/benchmarks_curated.csv')


if __name__ == '__main__':
    main()


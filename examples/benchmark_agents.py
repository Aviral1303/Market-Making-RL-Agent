import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from env.simple_lob_env import SimpleLOBEnv
from agents.naive_mm import NaiveMarketMaker
from agents.inventory_mm import InventoryAwareMarketMaker
from agents.avellaneda_stoikov import AvellanedaStoikovMM
from utils.metrics import sharpe, max_drawdown, hit_rate


def run_agent(agent, cfg, steps):
    env = SimpleLOBEnv(seed=cfg.get('seed'), market=cfg.get('market'), execution=cfg.get('execution'), fees=cfg.get('fees'))
    for _ in range(steps):
        bid, ask = agent.quote(env.mid_price, env.inventory)
        env.step(bid, ask)
    df = pd.DataFrame(env.history)
    returns = df['pnl'].diff().fillna(0.0).values
    return {
        'final_pnl': float(df['pnl'].iloc[-1]),
        'sharpe': sharpe(returns),
        'max_drawdown': max_drawdown(df['pnl'].values),
        'hit_rate': hit_rate(returns),
    }


def main():
    cfg = {
        'seed': 42,
        'steps': 1000,
        'market': {
            'ou_enabled': True,
            'ou': {'mu': 100.0, 'kappa': 0.05, 'sigma': 0.5, 'dt': 1.0},
            'vol_regime': {'enabled': True, 'high_sigma_scale': 3.0, 'switch_prob': 0.02},
        },
        'execution': {'base_arrival_rate': 1.0, 'alpha': 1.5},
        'fees': {'fee_bps': 1.0, 'slippage_bps': 2.0, 'maker_bps': -0.5, 'taker_bps': 1.0},
        'agent': {'spread': 0.10, 'inventory_sensitivity': 0.05},
    }
    steps = cfg['steps']

    results = {}
    results['naive'] = run_agent(NaiveMarketMaker(spread=cfg['agent']['spread']), cfg, steps)
    results['inventory'] = run_agent(
        InventoryAwareMarketMaker(spread=cfg['agent']['spread'], inventory_sensitivity=cfg['agent']['inventory_sensitivity']),
        cfg,
        steps,
    )
    results['avellaneda'] = run_agent(
        AvellanedaStoikovMM(risk_aversion=0.1, base_spread=cfg['agent']['spread'], inv_penalty=0.05), cfg, steps
    )

    df = pd.DataFrame(results).T
    print(df)

    labels = ['final_pnl', 'sharpe', 'max_drawdown']
    x = np.arange(len(labels))
    width = 0.25
    plt.figure(figsize=(10, 4))
    agents = list(results.keys())
    for i, name in enumerate(agents):
        vals = [results[name].get(k, 0) or 0 for k in labels]
        plt.bar(x + (i - 1) * width, vals, width, label=name)
    plt.xticks(x, labels)
    plt.legend()
    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/benchmark_agents.png')
    df.to_csv('results/benchmark_agents.csv', index=True)
    print('Saved results to results/benchmark_agents.csv and results/benchmark_agents.png')


if __name__ == '__main__':
    main()


import os
import pandas as pd
from adapters.market_replay import MarketReplay


def main():
    # Prepare a tiny sample if not present
    os.makedirs('data', exist_ok=True)
    sample = 'data/sample_trades.csv'
    if not os.path.exists(sample):
        pd.DataFrame([
            {'time': 1, 'mid': 100.0, 'best_bid': 99.9, 'best_ask': 100.1, 'volume': 1.0},
            {'time': 2, 'mid': 100.02, 'best_bid': 99.92, 'best_ask': 100.12, 'volume': 2.0},
            {'time': 3, 'mid': 99.98, 'best_bid': 99.88, 'best_ask': 100.08, 'volume': 1.5},
        ]).to_csv(sample, index=False)

    rep = MarketReplay(sample, fmt='csv')
    count = 0
    for tick in rep.iter_ticks():
        print(tick)
        count += 1
    print(f'Replayed {count} ticks from {sample}')


if __name__ == '__main__':
    main()


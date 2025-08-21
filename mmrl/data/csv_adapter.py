from __future__ import annotations

from typing import Iterator, Dict, Any, Optional
import pandas as pd

from .base import DataAdapter


class CSVAdapter(DataAdapter):
    """Generic CSV adapter with column mapping.

    Example mapping:
        {
          'time': 'timestamp',
          'mid_price': 'mid',
          'best_bid': 'bid',
          'best_ask': 'ask',
          'volume': 'qty'
        }
    """

    def __init__(self, path: str, mapping: Optional[Dict[str, str]] = None) -> None:
        self.df = pd.read_csv(path)
        self.mapping = mapping or {}

    def iter_ticks(self) -> Iterator[Dict[str, Any]]:
        for _, row in self.df.iterrows():
            tick: Dict[str, Any] = {}
            for k, v in self.mapping.items():
                tick[k] = row.get(v)
            yield tick


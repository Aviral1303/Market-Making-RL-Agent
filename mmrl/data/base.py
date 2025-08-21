from __future__ import annotations

from typing import Iterator, Dict, Any


class DataAdapter:
    """Base interface for user-provided data adapters.

    Implement `iter_ticks()` to yield dict ticks with keys that your env expects
    (e.g., time, mid_price, best_bid, best_ask, volume, etc.).
    """

    def iter_ticks(self) -> Iterator[Dict[str, Any]]:  # pragma: no cover - interface only
        raise NotImplementedError


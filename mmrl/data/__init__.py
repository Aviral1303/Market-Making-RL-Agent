from __future__ import annotations

import importlib
from typing import Any


def load_adapter(dotted_path: str, **params: Any):
    """Dynamically load a data adapter given a dotted path 'module:Class'."""
    if ":" not in dotted_path:
        raise ValueError("Adapter must be in 'module:Class' format")
    mod_name, cls_name = dotted_path.split(":", 1)
    module = importlib.import_module(mod_name)
    cls = getattr(module, cls_name)
    return cls(**params)


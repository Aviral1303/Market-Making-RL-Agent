import numpy as np 


def sharpe(returns: np.ndarray, risk_free: float = 0.0) -> float:
    returns = np.asarray(returns)
    if returns.size == 0:
        return 0.0
    excess = returns - risk_free
    std = excess.std(ddof=1)
    return float(excess.mean() / std) if std > 0 else 0.0


def max_drawdown(equity_curve: np.ndarray) -> float:
    equity = np.asarray(equity_curve)
    if equity.size == 0:
        return 0.0
    running_max = np.maximum.accumulate(equity)
    # Avoid division by zero
    denom = np.where(running_max == 0, 1.0, running_max)
    drawdowns = (equity - running_max) / denom
    return float(drawdowns.min())


def hit_rate(returns: np.ndarray) -> float:
    returns = np.asarray(returns)
    if returns.size == 0:
        return 0.0
    return float((returns > 0).mean())


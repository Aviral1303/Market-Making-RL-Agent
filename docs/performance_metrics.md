# Performance Metrics Guide

This guide explains the comprehensive performance metrics available in MMRL for analyzing market making strategies.

## Overview

MMRL provides industry-standard performance metrics that traders, researchers, and risk managers use to evaluate trading strategies. These metrics help you understand:

- **Return Performance**: How much money your strategy makes
- **Risk Metrics**: How much risk your strategy takes
- **Risk-Adjusted Returns**: How efficiently your strategy generates returns relative to risk
- **Trading Statistics**: How often your strategy wins vs. loses
- **Distribution Characteristics**: The shape and behavior of your returns

## Quick Start

```python
from utils.metrics import calculate_all_metrics, print_metrics_summary

# Calculate all metrics for your strategy returns
metrics = calculate_all_metrics(
    returns=your_returns_array,
    risk_free_rate=0.02,  # 2% annual risk-free rate
    periods_per_year=252   # Daily data
)

# Print a formatted summary
print_metrics_summary(metrics)
```

## Core Metrics

### 1. Return Metrics

#### Total Return
- **What it is**: The total percentage gain/loss over the entire period
- **Formula**: `(Final_Value / Initial_Value) - 1`
- **Interpretation**: Simple measure of absolute performance
- **Example**: 15.5% means your strategy grew by 15.5% over the period

#### Annualized Return
- **What it is**: The compound annual growth rate
- **Formula**: `(1 + Total_Return)^(Periods_Per_Year / Total_Periods) - 1`
- **Interpretation**: Standardized return measure for comparison across different time periods
- **Example**: 12.3% means your strategy grows at 12.3% per year on average

### 2. Risk Metrics

#### Volatility (Standard Deviation)
- **What it is**: Annualized standard deviation of returns
- **Formula**: `Std_Dev(Returns) × √(Periods_Per_Year)`
- **Interpretation**: Higher volatility = more uncertainty and potential for large losses
- **Example**: 25% means returns typically vary by ±25% annually

#### Maximum Drawdown
- **What it is**: Largest peak-to-trough decline in portfolio value
- **Formula**: `(Current_Value - Peak_Value) / Peak_Value`
- **Interpretation**: Measures the worst historical loss and recovery time needed
- **Example**: -18.5% means the strategy lost 18.5% from its peak at some point

#### Maximum Drawdown Duration
- **What it is**: How long the strategy took to recover from maximum drawdown
- **Interpretation**: Longer duration = more time spent underwater
- **Example**: 45 periods means it took 45 periods to recover from the worst loss

### 3. Risk-Adjusted Return Metrics

#### Sharpe Ratio
- **What it is**: Excess return per unit of total risk
- **Formula**: `(Return - Risk_Free_Rate) / Volatility`
- **Interpretation**: Higher is better; >1 is good, >2 is very good
- **Example**: 1.25 means you earn 1.25% excess return per 1% of volatility

#### Sortino Ratio
- **What it is**: Excess return per unit of downside risk
- **Formula**: `(Return - Risk_Free_Rate) / Downside_Deviation`
- **Interpretation**: Similar to Sharpe but only penalizes downside volatility
- **Example**: 1.8 means you earn 1.8% excess return per 1% of downside risk

#### Calmar Ratio
- **What it is**: Annualized return divided by maximum drawdown
- **Formula**: `Annualized_Return / |Max_Drawdown|`
- **Interpretation**: Higher is better; measures return relative to worst loss
- **Example**: 0.8 means annual return is 80% of the maximum drawdown

### 4. Trading Performance Metrics

#### Hit Rate (Win Rate)
- **What it is**: Percentage of periods with positive returns
- **Formula**: `Positive_Periods / Total_Periods`
- **Interpretation**: Higher is generally better, but not always (depends on risk/reward)
- **Example**: 65% means the strategy wins in 65% of periods

#### Profit Factor
- **What it is**: Ratio of gross profits to gross losses
- **Formula**: `Sum(Positive_Returns) / |Sum(Negative_Returns)|`
- **Interpretation**: >1 means profitable, >2 is very good
- **Example**: 1.8 means gross profits are 1.8x gross losses

### 5. Risk Management Metrics

#### Value at Risk (VaR)
- **What it is**: Maximum expected loss at a given confidence level
- **Formula**: Percentile of return distribution
- **Interpretation**: Lower (more negative) means higher risk
- **Example**: -2.5% means 95% of the time, you won't lose more than 2.5% in a period

#### Conditional Value at Risk (CVaR)
- **What it is**: Average loss when VaR threshold is exceeded
- **Formula**: Mean of returns below VaR threshold
- **Interpretation**: More conservative than VaR; considers tail risk
- **Example**: -3.2% means when you exceed VaR, you lose 3.2% on average

### 6. Distribution Metrics

#### Skewness
- **What it is**: Measure of return distribution asymmetry
- **Interpretation**: 
  - Positive: More positive outliers (good surprises)
  - Negative: More negative outliers (bad surprises)
  - Zero: Symmetric distribution
- **Example**: -0.5 means slightly more negative surprises than positive

#### Kurtosis
- **What it is**: Measure of "fat tails" in return distribution
- **Interpretation**: 
  - High: More extreme events than normal distribution
  - Low: Fewer extreme events
  - Normal distribution has kurtosis ≈ 0
- **Example**: 4.2 means more extreme events than a normal distribution

## Advanced Usage

### Rolling Metrics

Calculate metrics over rolling windows to see how performance changes over time:

```python
from utils.metrics import calculate_rolling_metrics

# Calculate 60-day rolling metrics
rolling_metrics = calculate_rolling_metrics(
    returns=your_returns,
    window=60,  # 60-day window
    periods_per_year=252
)

# Plot rolling Sharpe ratio
import matplotlib.pyplot as plt
plt.plot(rolling_metrics.index, rolling_metrics['rolling_sharpe'])
plt.title('Rolling Sharpe Ratio (60-day window)')
plt.show()
```

### Custom Risk-Free Rates

Adjust the risk-free rate based on your market and time period:

```python
# For US markets (Treasury rates)
metrics = calculate_all_metrics(
    returns=returns,
    risk_free_rate=0.05,  # 5% annual rate
    periods_per_year=252
)

# For different time frequencies
monthly_metrics = calculate_all_metrics(
    returns=monthly_returns,
    risk_free_rate=0.05,
    periods_per_year=12  # Monthly data
)
```

### Strategy Comparison

Compare multiple strategies side by side:

```python
strategies = {
    "Conservative": conservative_returns,
    "Balanced": balanced_returns,
    "Aggressive": aggressive_returns
}

comparison_data = []
for name, returns in strategies.items():
    metrics = calculate_all_metrics(returns)
    comparison_data.append({
        'Strategy': name,
        'Sharpe': f"{metrics['sharpe_ratio']:.2f}",
        'Max DD': f"{metrics['max_drawdown']:.2%}",
        'Hit Rate': f"{metrics['hit_rate']:.2%}"
    })

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df)
```

## Best Practices

### 1. Use Multiple Metrics
Don't rely on a single metric. Consider:
- **Return**: Total and annualized returns
- **Risk**: Volatility and maximum drawdown
- **Risk-Adjusted**: Sharpe, Sortino, and Calmar ratios
- **Risk Management**: VaR and CVaR
- **Trading**: Hit rate and profit factor

### 2. Consider Time Periods
- **Short-term**: Focus on volatility and drawdown
- **Long-term**: Emphasize annualized returns and risk-adjusted metrics
- **Rolling metrics**: Show how performance evolves over time

### 3. Benchmark Against Market
Compare your strategy to:
- Risk-free rate (Treasury bills)
- Market index (S&P 500, Russell 2000)
- Peer strategies or funds

### 4. Understand Limitations
- **Historical metrics** don't guarantee future performance
- **Out-of-sample testing** is crucial for validation
- **Market conditions** change, affecting metric stability

## Example Analysis

Here's a complete example analyzing a market making strategy:

```python
from utils.metrics import calculate_all_metrics, print_metrics_summary
import numpy as np

# Simulate strategy returns (replace with your actual data)
np.random.seed(42)
returns = np.random.normal(0.0008, 0.015, 1000)  # Daily returns

# Calculate comprehensive metrics
metrics = calculate_all_metrics(
    returns=returns,
    risk_free_rate=0.03,  # 3% annual risk-free rate
    periods_per_year=252   # Daily data
)

# Print summary
print_metrics_summary(metrics)

# Key insights
if metrics['sharpe_ratio'] > 1.0:
    print("✓ Good risk-adjusted returns")
else:
    print("⚠ Risk-adjusted returns could be improved")

if metrics['max_drawdown'] > -0.20:
    print("✓ Reasonable drawdown levels")
else:
    print("⚠ High drawdown risk")

if metrics['profit_factor'] > 1.5:
    print("✓ Strong profit generation")
else:
    print("⚠ Profit generation could be improved")
```

## Integration with MMRL

These metrics integrate seamlessly with MMRL's other components:

- **Environment Results**: Use metrics to evaluate simulation outcomes
- **Agent Comparison**: Compare different market making strategies
- **Hyperparameter Tuning**: Optimize strategies based on metrics
- **Risk Management**: Set limits based on VaR and drawdown metrics
- **Reporting**: Generate professional performance reports

## Next Steps

1. **Run the example**: Execute `examples/performance_analysis.py`
2. **Test your strategies**: Apply metrics to your own backtest results
3. **Customize metrics**: Modify or extend metrics for your specific needs
4. **Visualize results**: Create custom charts and dashboards
5. **Automate analysis**: Integrate metrics into your testing pipeline

For more advanced usage, see the API documentation and explore the source code in `utils/metrics.py`. 
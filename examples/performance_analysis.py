#!/usr/bin/env python3
"""
Performance Analysis Example for Market Making Strategies

This script demonstrates how to use the comprehensive performance metrics
to analyze market making strategy results.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add parent directory to path to import mmrl modules
sys.path.append(str(Path(__file__).parent.parent))

from utils.metrics import (
    calculate_all_metrics,
    calculate_rolling_metrics,
    print_metrics_summary,
    sharpe, sortino, max_drawdown, profit_factor
)


def generate_sample_returns(n_periods: int = 1000, seed: int = 42) -> np.ndarray:
    """
    Generate sample returns for demonstration purposes.
    
    Args:
        n_periods: Number of periods to generate
        seed: Random seed for reproducibility
    
    Returns:
        Array of returns
    """
    np.random.seed(seed)
    
    # Generate returns with some realistic characteristics
    # Daily returns with mean 0.0005 (about 12.6% annual) and std 0.02 (about 32% annual)
    returns = np.random.normal(0.0005, 0.02, n_periods)
    
    # Add some fat tails (kurtosis)
    extreme_events = np.random.choice([0, 1], size=n_periods, p=[0.98, 0.02])
    extreme_returns = np.random.normal(0, 0.05, n_periods)
    returns = np.where(extreme_events, extreme_returns, returns)
    
    # Add some negative skew (more negative surprises)
    negative_bias = np.random.choice([0, 1], size=n_periods, p=[0.95, 0.05])
    negative_returns = np.random.normal(-0.01, 0.03, n_periods)
    returns = np.where(negative_bias, negative_returns, returns)
    
    return returns


def analyze_strategy_performance(returns: np.ndarray, strategy_name: str = "Strategy") -> dict:
    """
    Analyze the performance of a trading strategy.
    
    Args:
        returns: Array of returns
        strategy_name: Name of the strategy for display
    
    Returns:
        Dictionary of calculated metrics
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING: {strategy_name}")
    print(f"{'='*60}")
    
    # Calculate all metrics
    metrics = calculate_all_metrics(
        returns=returns,
        risk_free_rate=0.02,  # 2% annual risk-free rate
        periods_per_year=252   # Daily data
    )
    
    # Print formatted summary
    print_metrics_summary(metrics)
    
    return metrics


def plot_performance_analysis(returns: np.ndarray, strategy_name: str = "Strategy"):
    """
    Create comprehensive performance analysis plots.
    
    Args:
        returns: Array of returns
        strategy_name: Name of the strategy for display
    """
    # Calculate equity curve
    equity_curve = np.cumprod(1 + returns)
    
    # Calculate rolling metrics
    rolling_metrics = calculate_rolling_metrics(returns, window=60)  # 60-day rolling window
    
    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Performance Analysis: {strategy_name}', fontsize=16)
    
    # 1. Equity Curve
    axes[0, 0].plot(equity_curve, label='Equity Curve', linewidth=2)
    axes[0, 0].set_title('Equity Curve')
    axes[0, 0].set_xlabel('Period')
    axes[0, 0].set_ylabel('Portfolio Value')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # 2. Returns Distribution
    axes[0, 1].hist(returns, bins=50, alpha=0.7, edgecolor='black')
    axes[0, 1].axvline(returns.mean(), color='red', linestyle='--', 
                       label=f'Mean: {returns.mean():.4f}')
    axes[0, 1].set_title('Returns Distribution')
    axes[0, 1].set_xlabel('Return')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # 3. Rolling Sharpe Ratio
    axes[1, 0].plot(rolling_metrics.index, rolling_metrics['rolling_sharpe'], 
                    label='Rolling Sharpe (60d)', linewidth=2)
    axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1, 0].axhline(y=1, color='green', linestyle='--', alpha=0.5, label='Sharpe = 1')
    axes[1, 0].set_title('Rolling Sharpe Ratio (60-day window)')
    axes[1, 0].set_xlabel('Period')
    axes[1, 0].set_ylabel('Sharpe Ratio')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # 4. Rolling Volatility
    axes[1, 1].plot(rolling_metrics.index, rolling_metrics['rolling_volatility'], 
                    label='Rolling Volatility (60d)', linewidth=2, color='orange')
    axes[1, 1].set_title('Rolling Volatility (60-day window)')
    axes[1, 1].set_xlabel('Period')
    axes[1, 1].set_ylabel('Annualized Volatility')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.show()


def compare_strategies(strategy_returns: dict):
    """
    Compare multiple strategies using key metrics.
    
    Args:
        strategy_returns: Dictionary mapping strategy names to return arrays
    """
    print(f"\n{'='*80}")
    print("STRATEGY COMPARISON")
    print(f"{'='*80}")
    
    comparison_data = []
    
    for strategy_name, returns in strategy_returns.items():
        metrics = calculate_all_metrics(returns, risk_free_rate=0.02, periods_per_year=252)
        
        comparison_data.append({
            'Strategy': strategy_name,
            'Total Return': f"{metrics['total_return']:.2%}",
            'Annualized Return': f"{metrics['annualized_return']:.2%}",
            'Volatility': f"{metrics['volatility']:.2%}",
            'Sharpe Ratio': f"{metrics['sharpe_ratio']:.2f}",
            'Sortino Ratio': f"{metrics['sortino_ratio']:.2f}",
            'Max Drawdown': f"{metrics['max_drawdown']:.2%}",
            'Hit Rate': f"{metrics['hit_rate']:.2%}",
            'Profit Factor': f"{metrics['profit_factor']:.2f}",
            'VaR (95%)': f"{metrics['var_95']:.2%}",
            'CVaR (95%)': f"{metrics['cvar_95']:.2%}"
        })
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.set_index('Strategy', inplace=True)
    
    # Display comparison table
    print(comparison_df.to_string())
    
    return comparison_df


def main():
    """Main function demonstrating the performance analysis capabilities."""
    print("Market Making Performance Analysis Example")
    print("=" * 50)
    
    # Generate sample data for different strategies
    print("\nGenerating sample data...")
    
    # Strategy 1: Conservative (lower risk, lower return)
    conservative_returns = generate_sample_returns(1000, seed=42)
    conservative_returns *= 0.7  # Scale down for conservative approach
    
    # Strategy 2: Aggressive (higher risk, higher return)
    aggressive_returns = generate_sample_returns(1000, seed=123)
    aggressive_returns *= 1.5  # Scale up for aggressive approach
    
    # Strategy 3: Balanced (moderate risk, moderate return)
    balanced_returns = generate_sample_returns(1000, seed=456)
    
    # Analyze each strategy
    strategies = {
        "Conservative": conservative_returns,
        "Balanced": balanced_returns,
        "Aggressive": aggressive_returns
    }
    
    all_metrics = {}
    for name, returns in strategies.items():
        metrics = analyze_strategy_performance(returns, name)
        all_metrics[name] = metrics
    
    # Compare strategies
    comparison_df = compare_strategies(strategies)
    
    # Create visualizations for one strategy (Balanced)
    print("\nCreating performance visualization for Balanced strategy...")
    plot_performance_analysis(balanced_returns, "Balanced Strategy")
    
    # Demonstrate individual metric calculations
    print(f"\n{'='*60}")
    print("INDIVIDUAL METRIC CALCULATIONS")
    print(f"{'='*60}")
    
    returns = balanced_returns
    print(f"Sharpe Ratio: {sharpe(returns, risk_free=0.02, periods_per_year=252):.3f}")
    print(f"Sortino Ratio: {sortino(returns, risk_free=0.02, periods_per_year=252):.3f}")
    print(f"Max Drawdown: {max_drawdown(np.cumprod(1 + returns)):.2%}")
    print(f"Profit Factor: {profit_factor(returns):.3f}")
    
    # Save comparison results
    output_file = "strategy_comparison.csv"
    comparison_df.to_csv(output_file)
    print(f"\nComparison results saved to: {output_file}")
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    print("This example demonstrates how to:")
    print("1. Calculate comprehensive performance metrics")
    print("2. Compare multiple strategies")
    print("3. Visualize performance over time")
    print("4. Generate rolling metrics for trend analysis")
    print("5. Export results for further analysis")


if __name__ == "__main__":
    main() 
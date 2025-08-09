import subprocess
from pathlib import Path
import typer

app = typer.Typer(help="Market Making RL CLI")


@app.command()
def backtest(config: str = typer.Option("configs/inventory.yaml", help="Path to YAML config")):
    """Run a single backtest using the given config."""
    # For now, experiments read configs/inventory.yaml directly.
    # Keeping the parameter for future pass-through.
    subprocess.run(["python3", "experiments/run_inventory_mm.py"], check=True)


@app.command()
def grid(config: str = typer.Option("configs/inventory.yaml", help="Path to YAML config")):
    """Run a grid search using the given config."""
    subprocess.run(["python3", "experiments/grid_search_inventory_mm.py"], check=True)


if __name__ == "__main__":
    app()
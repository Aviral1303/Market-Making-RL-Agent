# CLI entrypoint for "mmrl" using Typer
import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="Market Making RL CLI")


@app.command()
def backtest(config: str = typer.Option("configs/inventory.yaml", help="Path to YAML config")):
    # Run the existing experiment script
    subprocess.run(["python3", "experiments/run_inventory_mm.py"], check=True)


@app.command()
def grid(config: str = typer.Option("configs/inventory.yaml", help="Path to YAML config")):
    subprocess.run(["python3", "experiments/grid_search_inventory_mm.py"], check=True)


if __name__ == "__main__":
    app()

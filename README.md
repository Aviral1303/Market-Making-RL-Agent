# Market Making RL Agent

## Setup

1. Create/activate a virtualenv (recommended)
2. Install dependencies:

```
pip install -r requirements.txt
```

## Project Structure

- `env/`: Simulation environments
- `agents/`: Strategy and RL agents
- `experiments/`: Scripts to run simulations and grid searches
- `analysis/`: Analysis and plotting scripts
- `data/`: Generated CSVs
- `results/`: Generated plots

## Quickstart

- Run a single strategy simulation:
```
python3 experiments/run_inventory_mm.py
```
Outputs: `data/inventory_mm_run.csv`, `results/inventory_mm_plot.png`

- Run grid search over parameters:
```
python3 experiments/grid_search_inventory_mm.py
```
Outputs: `data/grid_search_results.csv`

- Plot grid heatmaps:
```
python3 analysis/plot_grid_heatmaps.py
```
Outputs: `results/grid_heatmaps.png`

## Notes
- Run commands from the project root so package imports resolve
- Python 3.10+ recommended

# Configuration

The main YAML file controls environment, execution, fees, and agent.

## Keys
- `run_tag` (str): MLflow experiment/run tag
- `seed` (int): global seed for determinism
- `steps` (int): number of timesteps
- `output_dir` (str): directory for results
- `market`:
  - `ou_enabled` (bool)
  - `ou`: `mu`, `kappa`, `sigma`, `dt`
  - `vol_regime`: `enabled`, `high_sigma_scale`, `switch_prob`
  - `correlation` (optional): NxN matrix (multi-asset)
- `execution`: `base_arrival_rate`, `alpha`, `size_sensitivity`
- `fees`: `fee_bps`, `slippage_bps`, `maker_bps`, `taker_bps`
- `agent`: `spread`, `inventory_sensitivity`
- `multi_asset` (optional): `num_assets`, `depth_levels`, `level_widen`, `base_size`, `regime_skew`
- `grid` (optional): sweep values for grid search

## Validate / Schema
```
mmrl config-validate
mmrl config-schema
```
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from pathlib import Path
import subprocess
import json
import time
from typing import List, Optional, Dict, Any
import yaml
import os
import tempfile
from prometheus_client import CollectorRegistry, Counter, generate_latest

app = FastAPI(title="MMRL API", version="0.1.0")

# Metrics
registry = CollectorRegistry()
RUNS_TOTAL = Counter("mmrl_runs_total", "Number of backtest runs", registry=registry)
GRIDS_TOTAL = Counter("mmrl_grids_total", "Number of grid runs", registry=registry)


def bearer_auth(token: Optional[str] = None):
    expected = os.environ.get("MMRL_API_TOKEN")
    if expected and token != f"Bearer {expected}":
        raise HTTPException(status_code=401, detail="unauthorized")


def get_run_dirs(results_root: Path = Path("results")) -> List[Path]:
    if not results_root.exists():
        return []
    run_dirs = [p for p in results_root.iterdir() if p.is_dir()]
    run_dirs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return run_dirs


def get_latest_run_dir(results_root: Path = Path("results")) -> Optional[Path]:
    run_dirs = get_run_dirs(results_root)
    return run_dirs[0] if run_dirs else None


def load_base_config() -> Dict[str, Any]:
    with open("configs/inventory.yaml", "r") as f:
        return yaml.safe_load(f)


def merge_overrides(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in (overrides or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge_overrides(out[k], v)
        else:
            out[k] = v
    return out


def run_with_config(cli_args: list[str], cfg: Optional[Dict[str, Any]] = None):
    env = os.environ.copy()
    tmpfile = None
    if cfg is not None:
        fd, path = tempfile.mkstemp(prefix="mmrl_cfg_", suffix=".yaml")
        with os.fdopen(fd, "w") as f:
            yaml.safe_dump(cfg, f, sort_keys=False)
        env["MMRL_CONFIG"] = path
        tmpfile = path
    try:
        subprocess.run(cli_args, check=True, env=env)
    finally:
        if tmpfile and Path(tmpfile).exists():
            try:
                Path(tmpfile).unlink()
            except Exception:
                pass


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(registry), media_type="text/plain; version=0.0.4")


@app.get("/runs")
def list_runs(limit: int = 20):
    runs = []
    for p in get_run_dirs()[:limit]:
        runs.append({
            "name": p.name,
            "path": str(p),
            "mtime": p.stat().st_mtime,
        })
    return {"runs": runs}


@app.get("/runs/{run_name}")
def get_run(run_name: str):
    run_path = Path("results") / run_name
    if not run_path.exists():
        raise HTTPException(status_code=404, detail="run not found")
    metrics = {}
    mp = run_path / "metrics.json"
    if mp.exists():
        try:
            metrics = json.loads(mp.read_text())
        except Exception:
            metrics = {}
    return {
        "run_dir": str(run_path),
        "metrics": metrics,
        "artifacts": {
            "config": str(run_path / "config.yaml"),
            "csv": str(run_path / "inventory_mm_run.csv"),
            "plot": str(run_path / "inventory_mm_plot.png"),
        },
    }


@app.post("/backtest")
def backtest(overrides: Optional[Dict[str, Any]] = Body(default=None), auth: None = Depends(bearer_auth)):
    cfg = None
    if overrides:
        base = load_base_config()
        cfg = merge_overrides(base, overrides)
    try:
        run_with_config(["mmrl", "backtest"], cfg)
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": f"backtest failed: {e}"})

    RUNS_TOTAL.inc()
    time.sleep(0.1)
    run_dir = get_latest_run_dir()
    if run_dir is None:
        return JSONResponse(status_code=500, content={"error": "no run directory found"})

    metrics_path = run_dir / "metrics.json"
    metrics = {}
    if metrics_path.exists():
        try:
            metrics = json.loads(metrics_path.read_text())
        except Exception:
            metrics = {}

    return {
        "run_dir": str(run_dir),
        "metrics": metrics,
        "artifacts": {
            "config": str(run_dir / "config.yaml"),
            "csv": str(run_dir / "inventory_mm_run.csv"),
            "plot": str(run_dir / "inventory_mm_plot.png"),
        },
    }


@app.post("/grid")
def grid(overrides: Optional[Dict[str, Any]] = Body(default=None), auth: None = Depends(bearer_auth)):
    cfg = None
    if overrides:
        base = load_base_config()
        cfg = merge_overrides(base, overrides)
    try:
        run_with_config(["mmrl", "grid"], cfg)
    except subprocess.CalledProcessError as e:
        return JSONResponse(status_code=500, content={"error": f"grid failed: {e}"})

    GRIDS_TOTAL.inc()
    time.sleep(0.1)
    run_dir = get_latest_run_dir()
    if run_dir is None:
        return JSONResponse(status_code=500, content={"error": "no run directory found"})

    csv_path = run_dir / "grid_search_results.csv"
    return {
        "run_dir": str(run_dir),
        "artifacts": {
            "config": str(run_dir / "config.yaml"),
            "csv": str(csv_path),
        },
    }
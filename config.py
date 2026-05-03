"""Global configuration for the agentic memory management simulation."""
from __future__ import annotations

from pathlib import Path

SEED: int = 42
TOTAL_MEMORY: int = 512
SEQUENCE_LENGTH: int = 250
PREDICTION_TOP_K: int = 2
THRASH_WINDOW: int = 3

APP_CATALOG = {
    "Chat": {"memory": 120, "load_time": 0.8},
    "Maps": {"memory": 180, "load_time": 1.2},
    "Music": {"memory": 90, "load_time": 0.5},
    "Camera": {"memory": 200, "load_time": 1.6},
    "Mail": {"memory": 110, "load_time": 0.7},
    "Browser": {"memory": 160, "load_time": 1.1},
}

RESULTS_DIR: Path = Path("results")
CSV_RESULTS_PATH: Path = RESULTS_DIR / "experiment_results.csv"
PLOT_LOAD_TIME_PATH: Path = RESULTS_DIR / "load_time_vs_method.png"
PLOT_HIT_RATE_PATH: Path = RESULTS_DIR / "cache_hit_rate_vs_method.png"
PLOT_MEMORY_PATH: Path = RESULTS_DIR / "memory_usage_vs_method.png"

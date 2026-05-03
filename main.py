"""Entry point for running the agentic memory management experiments."""
from __future__ import annotations

from config import (
    APP_CATALOG,
    CSV_RESULTS_PATH,
    PLOT_HIT_RATE_PATH,
    PLOT_LOAD_TIME_PATH,
    PLOT_MEMORY_PATH,
    PREDICTION_TOP_K,
    RESULTS_DIR,
    SEED,
    SEQUENCE_LENGTH,
    THRASH_WINDOW,
    TOTAL_MEMORY,
)
from experiments.run_experiments import run_all
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def main() -> None:
    """Run the experiments with default configuration."""
    results = run_all(
        app_config=APP_CATALOG,
        total_memory=TOTAL_MEMORY,
        sequence_length=SEQUENCE_LENGTH,
        seed=SEED,
        thrash_window=THRASH_WINDOW,
        prediction_top_k=PREDICTION_TOP_K,
        results_dir=RESULTS_DIR,
    )
    LOGGER.info("Saved CSV to %s", CSV_RESULTS_PATH)
    LOGGER.info("Saved plots to %s, %s, %s", PLOT_LOAD_TIME_PATH, PLOT_HIT_RATE_PATH, PLOT_MEMORY_PATH)
    LOGGER.info("Final comparison table:\n%s", results.to_string(index=False))


if __name__ == "__main__":
    main()

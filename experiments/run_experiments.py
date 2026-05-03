"""Run simulations comparing baseline and agentic strategies."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from agents.allocator_agent import AllocatorAgent
from agents.cache_agent import CacheAgent
from agents.eviction_agent import EvictionAgent
from agents.planner_agent import PlannerAgent
from baselines.fifo import FIFOBaseline
from baselines.lru import LRUBaseline
from models.predictor import MarkovPredictor
from simulator.app import App
from simulator.environment import MemoryEnvironment
from utils.logger import get_logger
from utils.metrics import MetricsSummary, SimulationMetrics

LOGGER = get_logger(__name__)


def build_app_catalog(app_config: Dict[str, Dict[str, float]]) -> Dict[str, App]:
    """Create App objects from configuration."""
    return {
        name: App(name=name, memory_usage=int(cfg["memory"]), load_time=float(cfg["load_time"]))
        for name, cfg in app_config.items()
    }


def reset_catalog(app_catalog: Dict[str, App]) -> None:
    """Reset app states between simulation runs."""
    for app in app_catalog.values():
        app.unload()


def generate_sequence(app_names: List[str], length: int, seed: int) -> List[str]:
    """Generate an app usage sequence using a random Markov process."""
    rng = np.random.default_rng(seed)
    n = len(app_names)
    transition = rng.dirichlet(np.ones(n), size=n)
    current = int(rng.integers(0, n))
    sequence = []
    for _ in range(length):
        sequence.append(app_names[current])
        current = int(rng.choice(n, p=transition[current]))
    return sequence


def run_baseline(
    sequence: Iterable[str],
    app_catalog: Dict[str, App],
    total_memory: int,
    thrash_window: int,
    baseline: str,
) -> MetricsSummary:
    """Run a baseline policy simulation."""
    env = MemoryEnvironment(total_memory)
    metrics = SimulationMetrics(thrash_window)
    policy = LRUBaseline() if baseline == "LRU" else FIFOBaseline()
    for step, app_name in enumerate(sequence):
        app = app_catalog[app_name]
        hit, load_time, evicted = policy.handle_access(app, env, step)
        for evicted_app in evicted:
            metrics.record_eviction(evicted_app, step)
        metrics.record_access(app_name, hit, load_time, env.current_usage, step)
    return metrics.summarize()


def run_agentic(
    sequence: Iterable[str],
    app_catalog: Dict[str, App],
    total_memory: int,
    thrash_window: int,
    prediction_top_k: int,
) -> MetricsSummary:
    """Run the agentic multi-agent memory manager."""
    env = MemoryEnvironment(total_memory)
    metrics = SimulationMetrics(thrash_window)

    predictor = MarkovPredictor(app_catalog.keys())
    planner = PlannerAgent()
    allocator = AllocatorAgent()
    eviction_agent = EvictionAgent()
    cache_agent = CacheAgent()

    previous_app: str | None = None

    for step, app_name in enumerate(sequence):
        if previous_app is not None:
            predictor.update(previous_app, app_name)
        predictions = predictor.predict_top_k(previous_app, prediction_top_k)
        plan = planner.plan(predictions, env.get_state())
        evicted = allocator.allocate(
            env,
            plan,
            app_catalog,
            cache_agent,
            eviction_agent,
            step,
        )
        for evicted_app in evicted:
            metrics.record_eviction(evicted_app, step)

        app = app_catalog[app_name]
        hit = app.name in env.loaded_apps
        if hit:
            app.last_accessed = step
            cache_agent.touch(app.name)
            load_time = 0.0
        else:
            if not env.can_fit(app):
                new_evicted = eviction_agent.evict_for_app(
                    env, app, cache_agent, protected=plan.keep
                )
                for evicted_app in new_evicted:
                    metrics.record_eviction(evicted_app, step)
                evicted.extend(new_evicted)
            if env.can_fit(app):
                env.load_app(app, step)
                cache_agent.touch(app.name)
                load_time = app.load_time
            else:
                load_time = app.load_time
        metrics.record_access(app_name, hit, load_time, env.current_usage, step)
        previous_app = app_name
    return metrics.summarize()


def plot_metric(results: pd.DataFrame, metric: str, path: Path) -> None:
    """Plot a single metric for each method."""
    plt.figure(figsize=(6, 4))
    colors = plt.get_cmap("tab10").colors
    plt.bar(results["method"], results[metric], color=colors[: len(results)])
    plt.ylabel(metric.replace("_", " ").title())
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def run_all(
    app_config: Dict[str, Dict[str, float]],
    total_memory: int,
    sequence_length: int,
    seed: int,
    thrash_window: int,
    prediction_top_k: int,
    results_dir: Path,
) -> pd.DataFrame:
    """Run the full experiment suite and return the results table."""
    results_dir.mkdir(parents=True, exist_ok=True)
    app_catalog = build_app_catalog(app_config)
    sequence = generate_sequence(list(app_catalog.keys()), sequence_length, seed)

    reset_catalog(app_catalog)
    lru_summary = run_baseline(sequence, app_catalog, total_memory, thrash_window, "LRU")

    reset_catalog(app_catalog)
    fifo_summary = run_baseline(sequence, app_catalog, total_memory, thrash_window, "FIFO")

    reset_catalog(app_catalog)
    agentic_summary = run_agentic(
        sequence,
        app_catalog,
        total_memory,
        thrash_window,
        prediction_top_k,
    )

    summaries = {"LRU": lru_summary, "FIFO": fifo_summary, "Agentic": agentic_summary}

    rows = [{"method": method, **asdict(summary)} for method, summary in summaries.items()]
    results = pd.DataFrame(rows)

    results.to_csv(results_dir / "experiment_results.csv", index=False)
    plot_metric(results, "average_load_time", results_dir / "load_time_vs_method.png")
    plot_metric(results, "cache_hit_rate", results_dir / "cache_hit_rate_vs_method.png")
    plot_metric(results, "average_memory_usage", results_dir / "memory_usage_vs_method.png")

    LOGGER.info("Experiment results:\n%s", results.to_string(index=False))
    return results

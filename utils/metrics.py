"""Metrics tracking for memory management experiments."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class MetricsSummary:
    """Summary statistics for a simulation run.

    average_memory_usage reflects the mean of memory usage snapshots per access.
    """

    average_load_time: float
    cache_hit_rate: float
    average_memory_usage: float
    thrash_count: int


class SimulationMetrics:
    """Track simulation metrics such as load times and thrashing."""

    def __init__(self, thrash_window: int) -> None:
        self.thrash_window = thrash_window
        self.total_accesses = 0
        self.total_load_time = 0.0
        self.cache_hits = 0
        self.memory_usage_sum = 0.0
        self.thrash_count = 0
        self.eviction_steps: Dict[str, int] = {}

    def record_access(
        self,
        app_name: str,
        hit: bool,
        load_time: float,
        current_usage: int,
        step: int,
    ) -> None:
        """Record an app access event."""
        self.total_accesses += 1
        self.total_load_time += load_time
        self.memory_usage_sum += current_usage
        if hit:
            self.cache_hits += 1
        else:
            last_evicted = self.eviction_steps.get(app_name)
            if last_evicted is not None and step - last_evicted <= self.thrash_window:
                self.thrash_count += 1

    def record_eviction(self, app_name: str, step: int) -> None:
        """Record an eviction event."""
        self.eviction_steps[app_name] = step

    def summarize(self) -> MetricsSummary:
        """Summarize metrics into a MetricsSummary object."""
        if self.total_accesses == 0:
            return MetricsSummary(0.0, 0.0, 0.0, self.thrash_count)
        return MetricsSummary(
            average_load_time=self.total_load_time / self.total_accesses,
            cache_hit_rate=self.cache_hits / self.total_accesses,
            average_memory_usage=self.memory_usage_sum / self.total_accesses,
            thrash_count=self.thrash_count,
        )

"""Eviction agent responsible for selecting apps to evict."""
from __future__ import annotations

from typing import Iterable, List

from agents.cache_agent import CacheAgent
from simulator.app import App
from simulator.environment import MemoryEnvironment


class EvictionAgent:
    """Evicts apps to free memory based on cache recency."""

    def evict_for_app(
        self,
        env: MemoryEnvironment,
        app: App,
        cache_agent: CacheAgent,
        protected: Iterable[str],
    ) -> List[str]:
        """Evict apps until the target app fits, returning evicted app names."""
        evicted: List[str] = []
        while not env.can_fit(app):
            victim = cache_agent.least_recently_used(protected)
            if victim is None:
                break
            env.evict_app(victim)
            cache_agent.remove(victim)
            evicted.append(victim)
        return evicted

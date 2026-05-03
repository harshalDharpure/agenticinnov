"""Allocator agent responsible for ensuring memory for planned preloads."""
from __future__ import annotations

from typing import Dict, Iterable, List

from agents.cache_agent import CacheAgent
from agents.eviction_agent import EvictionAgent
from agents.planner_agent import Plan
from simulator.app import App
from simulator.environment import MemoryEnvironment


class AllocatorAgent:
    """Ensures enough memory is available for planned actions."""

    def allocate(
        self,
        env: MemoryEnvironment,
        plan: Plan,
        app_catalog: Dict[str, App],
        cache_agent: CacheAgent,
        eviction_agent: EvictionAgent,
        step: int,
    ) -> List[str]:
        """Execute allocations for preload plan and return evicted apps."""
        evicted: List[str] = []
        for app_name in plan.preload:
            app = app_catalog[app_name]
            evicted.extend(
                eviction_agent.evict_for_app(env, app, cache_agent, protected=plan.keep)
            )
            if env.load_app(app, step):
                cache_agent.touch(app_name)
        return evicted

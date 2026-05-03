"""LRU cache baseline."""
from __future__ import annotations

from collections import OrderedDict
from typing import Dict, List, Tuple

from simulator.app import App
from simulator.environment import MemoryEnvironment


class LRUBaseline:
    """Least-recently-used cache baseline."""

    def __init__(self) -> None:
        self.recency: "OrderedDict[str, None]" = OrderedDict()

    def handle_access(
        self, app: App, env: MemoryEnvironment, step: int
    ) -> Tuple[bool, float, List[str]]:
        """Handle an app access and return (hit, load_time, evicted_apps)."""
        hit = app.name in env.loaded_apps
        evicted: List[str] = []
        if not hit:
            while not env.can_fit(app):
                evicted_name = self._select_eviction()
                if evicted_name is None:
                    break
                env.evict_app(evicted_name)
                self.recency.pop(evicted_name, None)
                evicted.append(evicted_name)
            env.load_app(app, step)
        self._touch(app.name)
        load_time = 0.0 if hit else app.load_time
        return hit, load_time, evicted

    def _touch(self, app_name: str) -> None:
        """Update recency ordering for an app."""
        if app_name in self.recency:
            self.recency.move_to_end(app_name)
        else:
            self.recency[app_name] = None

    def _select_eviction(self) -> str | None:
        """Select the least recently used app to evict."""
        if not self.recency:
            return None
        return next(iter(self.recency.keys()))

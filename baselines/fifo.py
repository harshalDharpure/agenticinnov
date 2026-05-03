"""FIFO cache baseline."""
from __future__ import annotations

from collections import deque
from typing import Deque, List, Tuple

from simulator.app import App
from simulator.environment import MemoryEnvironment


class FIFOBaseline:
    """First-in-first-out cache baseline."""

    def __init__(self) -> None:
        self.queue: Deque[str] = deque()

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
                if evicted_name in self.queue:
                    self.queue.remove(evicted_name)
                evicted.append(evicted_name)
            env.load_app(app, step)
            self.queue.append(app.name)
        load_time = 0.0 if hit else app.load_time
        return hit, load_time, evicted

    def _select_eviction(self) -> str | None:
        """Select the oldest app to evict."""
        if not self.queue:
            return None
        return self.queue.popleft()

"""Simulation environment for app memory management."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from simulator.app import App


@dataclass
class EnvironmentState:
    """Snapshot of the current memory state."""

    total_memory: int
    current_usage: int
    loaded_apps: List[str]


class MemoryEnvironment:
    """Environment tracking memory usage and loaded apps."""

    def __init__(self, total_memory: int) -> None:
        self.total_memory = total_memory
        self.current_usage = 0
        self.loaded_apps: Dict[str, App] = {}

    def can_fit(self, app: App) -> bool:
        """Return True if the app fits into memory without eviction."""
        return self.current_usage + app.memory_usage <= self.total_memory

    def load_app(self, app: App, step: int) -> bool:
        """Load an app if memory allows.

        Returns True only when the app is newly loaded into memory.
        """
        if app.name in self.loaded_apps:
            app.last_accessed = step
            return False
        if not self.can_fit(app):
            return False
        self.loaded_apps[app.name] = app
        self.current_usage += app.memory_usage
        app.load(step)
        return True

    def evict_app(self, app_name: str) -> App | None:
        """Evict an app by name and return it if present."""
        app = self.loaded_apps.pop(app_name, None)
        if app is None:
            return None
        self.current_usage -= app.memory_usage
        app.unload()
        return app

    def switch_app(self, app: App, step: int) -> bool:
        """Access an app, returning True on cache hit, False on miss."""
        if app.name in self.loaded_apps:
            app.last_accessed = step
            return True
        return self.load_app(app, step)

    def get_state(self) -> EnvironmentState:
        """Return a snapshot of the environment state."""
        return EnvironmentState(
            total_memory=self.total_memory,
            current_usage=self.current_usage,
            loaded_apps=list(self.loaded_apps.keys()),
        )

    def loaded_app_objects(self) -> Iterable[App]:
        """Return loaded app objects."""
        return self.loaded_apps.values()
